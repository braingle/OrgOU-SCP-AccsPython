import boto3
import csv

# Create a boto3 client for AWS Organizations
org_client = boto3.client('organizations')

# Get a list of all accounts in the organization
response = org_client.list_accounts()
accounts = response['Accounts']

# Open a CSV file to write the results to
with open('aws_accounts.csv', mode='w') as csv_file:
    fieldnames = ['Account Name', 'Account ID', 'Organizational Unit', 'Service Control Policies']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    # Loop through each account and retrieve the OU and SCPs associated with it
    for account in accounts:
        account_id = account['Id']
        account_name = account['Name']

        # Retrieve the OUs that the account is a member of
        response = org_client.list_parents(ChildId=account_id)
        ou_list = response['Parents']

        # If the account is not a member of any OUs, set the OU name to 'None'
        ou_name = 'None' if not ou_list else ou_list[0].get('Name', 'None')

        # Retrieve the SCPs associated with the account
        response = org_client.list_policies_for_target(TargetId=account_id, Filter='SERVICE_CONTROL_POLICY')
        scps = response['Policies']

        # If the account is not associated with any SCPs, set the SCP names to 'None'
        scp_names = [scp['Name'] for scp in scps] if scps else ['None']

        # Write the account, OU, and SCP information to the CSV file
        writer.writerow({
            'Account Name': account_name,
            'Account ID': account_id,
            'Organizational Unit': ou_name,
            'Service Control Policies': ';'.join(scp_names)
        })
