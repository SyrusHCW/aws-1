import requests
import json
import random
import string
import boto3


def lambda_handler(event, context):
    print(event)
    json_input = event
    
    region = json_input['region']
    env_name = json_input['env_name']
    acct_id = json_input['acct_id']
    palo_cred = 9
    if acct_id == "":
        aws_cred = 16
    
    aws_access_key = ''
    aws_secret_key = ''

    dynamodb = boto3.resource('dynamodb',
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_key,
        region_name = region
        )
 
    #print(interface)
    
    ###### Update AZ1 Table Tunnel 1 #####################
    table = dynamodb.Table('USE1-LE-TRANSIT-AZ1')
    data = table.scan()
    ip_count = len(data['Items'])
    top = ip_count - 1
    new_net = data['Items'][top]['host_bits'] + 1
    vpn_cidr = '{0}{1}'.format(data['Items'][top]['network_bits'], new_net)
    new_int = data['Items'][top - 1]['interface'] +1
    interface1 = new_int
    interface2 = interface1 + 1
    bgpASN = int(data['Items'][top]['bgpASN'])
    bgp_asn = bgpASN + 1
    print(vpn_cidr)

    new_aws = new_net + 1
    new_pa = new_aws + 1
    new_brd = new_pa + 1

    vpc_name = '{0}{1}'.format(env_name, '-VPC')

    tun_net1_cidrAZ1 = '{0}{1}{2}'.format(data['Items'][top]['network_bits'], new_net, '/30')

    
    ###### Update AZ1 Table Tunnel 2 #####################

    new_net = new_brd + 1
    new_aws = new_net + 1
    new_pa = new_aws + 1
    new_brd = new_pa + 1

    vpc_name = '{0}{1}'.format(env_name, '-VPC')
    
    tun_net2_cidrAZ1 = '{0}{1}{2}'.format(data['Items'][top]['network_bits'], new_net, '/30')



    ###### Update AZ2 Table tunnel 1 #####################
    table = dynamodb.Table('USE1-LE-TRANSIT-AZ2')
    data = table.scan()
    ip_count = len(data['Items'])
    top = ip_count - 1
    new_net = data['Items'][top]['host_bits'] + 1
    vpn_cidr = '{0}{1}'.format(data['Items'][top]['network_bits'], new_net)
    print(vpn_cidr)

    new_aws = new_net + 1
    new_pa = new_aws + 1
    new_brd = new_pa + 1

    vpc_name = '{0}{1}'.format(env_name, '-VPC')

    
    tun_net1_cidrAZ2 = '{0}{1}{2}'.format(data['Items'][top]['network_bits'], new_net, '/30')
    


    ###### Update AZ2 Table tunnel 2 #####################
    new_net = new_brd + 1
    new_aws = new_net + 1
    new_pa = new_aws + 1
    new_brd = new_pa + 1

    vpc_name = '{0}{1}'.format(env_name, '-VPC')
    
    tun_net2_cidrAZ2 = '{0}{1}{2}'.format(data['Items'][top]['network_bits'], new_net, '/30')
    

    role = '{0}{1}'.format(env_name, ' VPN palo alto address tunnel 2')


    
    creds = '{0}{1}'.format(acct_id, '-svc-ansible')
    vpc_name = '{0}{1}'.format(env_name, '-VPC')
    random1 = ''.join([random.choice(string.ascii_letters + string.digits)for n in range(32)])
    
    extra_vars = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}{16}{17}{18}{19}'.format("interface1_id: ", interface1, "\ninterface2_id: ", interface2, "\nspoke_asn: ", bgp_asn, "\nregion: ", region, "\naz1_tunnelinsidecidr1: ", tun_net1_cidrAZ1, "\naz1_tunnelinsidecidr2: ", tun_net2_cidrAZ1, "\naz2_tunnelinsidecidr1: ", tun_net1_cidrAZ2, "\naz2_tunnelinsidecidr2: ", tun_net2_cidrAZ2, "\npsk: ", random1, "\nacct_id: ", acct_id)
    
    print(extra_vars)
    
    data = { 'creds': [palo_cred, aws_cred], 'extra_vars': extra_vars }
    headers = {'Content-Type': 'application/json'}
    session = requests.Session()
    print(extra_vars)
    response = session.post('https://acme.com/api/v2/job_templates/38/launch/', verify=False, auth=('username', 'password'), headers=headers, json=data)

    print(list(response))
