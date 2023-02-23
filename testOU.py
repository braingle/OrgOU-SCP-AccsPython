import boto3
import csv

# Create an Organizations client
orgs_client = boto3.client('organizations')

# Get a list of all accounts in the organization
accounts = orgs_client.list_accounts()

# Initialize a list to hold the data
account_data = []

# Iterate through each account and get its details
for account in accounts['Accounts']:
    # Get the account ID and name
    account_id = account['Id']
    account_name = account['Name']

    # Get the list of OUs to which the account is associated
    response = orgs_client.describe_organization()
    ou_id = response['Organization']['Id']
    print(response)
    print(ou_id)
    ou_response = orgs_client.list_parents(ChildId=account_id)
    print(ou_response)
    ou_Id = [ou['Id'] for ou in ou_response.get('Parents', [])
                if ou.get('Type') == 'ORGANIZATIONAL_UNIT']
    print(ou_Id)            
    if not ou_Id:
        ou_Id = ['None']

    # Get the list of SCPs by which the account is tied with
    scp_response = orgs_client.list_policies_for_target(
        TargetId=account_id, Filter='SERVICE_CONTROL_POLICY')
    scp_names = [scp['Name'] for scp in scp_response.get('Policies', [])]
    if not scp_names:
        scp_names = ['None']

    # Add the account data to the list
    account_data.append([account_id, account_name, ou_id, scp_names])
    #print(account_data)

# Export the data to a CSV file
with open('account_data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Account ID', 'Account Name', 'OU Id', 'SCP Names'])
    writer.writerows(account_data)
