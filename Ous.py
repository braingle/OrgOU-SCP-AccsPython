import boto3
import csv

# Create a boto3 client for AWS Organizations
org_client = boto3.client('organizations')

# Get the root of the organization
response = org_client.describe_organization()
root_id = response['Organization']['MasterAccountId']
#print(response)
#print(root_id)

# Get a list of all OUs in the organization
response = org_client.list_roots()
root = response['Roots'][0]
ou_response = org_client.list_children(ParentId=root['Id'], ChildType='ORGANIZATIONAL_UNIT')
ous = ou_response['Children']
#print(response)
#print(root)
#print(ous)
# Open a CSV file to write the results to
with open('aws_accounts.csv', mode='w') as csv_file:
    fieldnames = ['Account Name', 'Account ID', 'Organizational Unit ID', 'Organizational Unit Name']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    # Loop through each OU and retrieve the accounts that are members of it
    for ou in ous:
        ou_id = ou['Id']
        ou_name = ou['Name']
        print(ou_id)
        print(ou_name)

        response = org_client.list_accounts_for_parent(ParentId=ou_id)
        accounts = response['Accounts']
        #print(f"OU Name: {ou_name}, OU ID: {ou_id}, Accounts: {accounts}")
        print(accounts)

        # Write the account and OU information to the CSV file
        for account in accounts:
            account_name = account['Name']
            account_id = account['Id']

            writer.writerow({
                'Account Name': account_name,
                'Account ID': account_id,
                'Organizational Unit ID': ou_id,
                'Organizational Unit Name': ou_name
            })
