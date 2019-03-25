import sendRequests
import datetime
import json
import sendRequests


def scan_ip(ip, key):
    result = {}
    url = "https://api.apility.net/v2.0/ip/{0}".format(ip)
    params = {'items': 200, 'token': key}
    data = sendRequests.sendGETrequest(url, myparams=params)
    if data:
        #print(json.dumps(data, indent=4))
        data = data['fullip']
        hostname = data['hostname']  # Reverse DNS lookup

        print("[apility.io] [%s] Checking Domain" % ip)
        if data['baddomain']['domain']['score'] < 0:
            if not hostname:
                hostname = "HOSTNAME_NOT_FOUND"
            result[hostname] = {'Blacklist': []}

            if data['baddomain']['domain']['blacklist']:
                result[hostname]['Blacklist'].extend(data['baddomain']['domain']['blacklist'])
            if data['baddomain']['domain']['blacklist_mx']:
                result[hostname]['Blacklist'].extend(data['baddomain']['domain']['blacklist_mx'])
            if data['baddomain']['domain']['blacklist_ns']:
                result[hostname]['Blacklist'].extend(data['baddomain']['domain']['blacklist_ns'])
            if data['baddomain']['domain']['mx']:
                result[hostname]['MX'] = data['baddomain']['domain']['mx']
            if data['baddomain']['domain']['ns']:
                result[hostname]['NS'] = data['baddomain']['domain']['ns']

            if result[hostname]['Blacklist']:
                result[hostname]['Blacklist'] = list(set(result[hostname]['Blacklist']))

        print("[apility.io] [%s] Checking IP associated with domain" % ip)
        if data['baddomain']['ip']:
            if data['baddomain']['ip']['score'] < 0:
                result[data['baddomain']['ip']['address']] = {'Blaclist': data['baddomain']['ip']['blacklist']}

        print("[apility.io] [%s] Checking Source IP associated with domain" % ip)
        if data['baddomain']['source_ip']:
            if data['baddomain']['source_ip']['score'] < 0:
                result[data['baddomain']['source_ip']['address']] = {'Blacklist': data['baddomain']['source_ip']['blacklist']}

        print("[apility.io] [%s] Checking History" % ip)
        if data['history']:
            if data['history']['score'] < 0:
                result['historical_activity'] = {}
                result['historical_activity']['Days Ago'] = []
                result['historical_activity']['Blacklist'] = []
                for activity in data['history']['activity']:
                    filtered_activity = {}
                    filtered_activity['changed_since_days'] = (datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - datetime.datetime.utcfromtimestamp(activity['timestamp']/1000).replace(tzinfo=datetime.timezone.utc)).days
                    result['historical_activity']['Days Ago'].append(filtered_activity['changed_since_days'])
                    result['historical_activity']['Blacklist'].append(activity['blacklists'])
                result['historical_activity']['Days Ago'] = list(set(result['historical_activity']['Days Ago']))
                result['historical_activity']['Blacklist'] = list(set(result['historical_activity']['Blacklist']))

        print("[apility.io] [%s] Getting Geo Info" % ip)
        if data['geo']:
            result['Geo'] = {'Latitude': data['geo']['latitude'], 'Longitude': data['geo']['longitude'], 'Country': data['geo']['country'], 'City': data['geo']['city'], 'Region': data['geo']['region']}

        print("[apility.io] [%s] Getting WHOIS" % ip)
        if data['whois']:
            result['whois'] = data['whois']
    return result


def scan_url(domains, key):
    result = {}
    url = "https://api.apility.net/baddomain_batch/%s" % domains
    params = {'token': key}
    data = sendRequests.sendGETrequest(url, myparams=params)
    if data:
        for each_url in data:
            if each_url['scoring']['source_ip']:
                print("[apility.io] Checking source IP %s associated with domain %s" % (
                each_url['scoring']['source_ip']['address'], each_url['domain']))
                if each_url['scoring']['source_ip']['score'] < 0:
                    result[each_url['scoring']['source_ip']['address']] = {'Blacklist': each_url['scoring']['source_ip']['blacklist']}

                print("[apility.io] Checking IP %s associated with domain %s" % (
                each_url['scoring']['ip']['address'], each_url['domain']))
                if each_url['scoring']['ip']['score'] < 0:
                    result[each_url['scoring']['ip']['address']] = {'Blacklist': each_url['scoring']['ip']['blacklist']}

                print("[apility.io] Checking domain %s" % each_url['domain'])
                if each_url['scoring']['domain']['score'] < 0:
                    result['Blacklist'] = each_url['scoring']['domain']['blacklist']
                    if each_url['scoring']['domain']['blacklist_mx']:
                        result['Blacklist'].extend(each_url['scoring']['domain']['blacklist_mx'])
                    if each_url['scoring']['domain']['blacklist_ns']:
                        result['Blacklist'].extend(each_url['scoring']['domain']['blacklist_ns'])
                    result['Blacklist'] = list(set(result['Blacklist']))
                    if each_url['scoring']['domain']['ns']:
                        result['MX'] = each_url['scoring']['domain']['ns']
                    if each_url['scoring']['domain']['mx']:
                        result['NS'] = each_url['scoring']['domain']['mx']
    return result


def scan_email(emails, key):
    result = {}
    url = "https://api.apility.net/bademail_batch/%s" % emails
    params = {'token': key}
    data = sendRequests.sendGETrequest(url, myparams=params)
    if data:
        for each_email in data:
            print("[apility.io] Checking SMTP associated with email %s" % each_email['email'])
            if each_email['scoring']['smtp']['score']:
                if each_email['scoring']['smtp']['exist_mx']:
                    result['SMTP Reachable'] = True

            print("[apility.io] Checking domain %s" % each_email['email'])
            if each_email['scoring']['domain']['score'] < 0:
                result['Blacklist'] = each_email['scoring']['domain']['blacklist']
                result['Blacklist'].extend(each_email['scoring']['domain']['blacklist_mx'])
                result['Blacklist'].extend(each_email['scoring']['domain']['blacklist_ns'])
                result['Blacklist'] = list(set(result['Blacklist']))
                if each_email['scoring']['domain']['ns']:
                    result['NS'] = each_email['scoring']['domain']['ns']
                if each_email['scoring']['domain']['mx']:
                    result['MX'] = each_email['scoring']['domain']['mx']

            print("[apility.io] Checking IP %s associated with email %s" % (
            each_email['scoring']['ip']['address'], each_email['email']))
            if each_email['scoring']['ip']['score'] < 0:
                result[each_email['scoring']['ip']['address']] = {'Blacklist': each_email['scoring']['ip']['blacklist']}

            print("[apility.io] Checking source IP %s associated with email %s" % (
            each_email['scoring']['source_ip']['address'], each_email['email']))
            if each_email['scoring']['source_ip']['score'] < 0:
                result[each_email['scoring']['source_ip']['address']] = {'Blacklist': each_email['scoring']['source_ip']['blacklist']}

            print("[apility.io] Checking freemail list for email %s" % each_email['email'])
            if each_email['scoring']['freemail']['is_freemail']:
                result['Free Email'] = True

            print("[apility.io] Checking Disposable Email Address Providers list for email %s" % each_email['email'])
            if each_email['scoring']['disposable']['is_disposable']:
                result['Disposable Email'] = True

            print("[apility.io] Checking email")
            if each_email['scoring']['email']['score'] < 0:
                result['Blacklist'].extend(each_email['scoring']['email']['blacklist'])
                result['Blacklist'] = list(set(result['Blacklist']))
    return result


def main(ioc, key):
    result = {}
    '''
    if ioc is ip:
        result = scan_ip(ip, key)
    if ioc is domain:
        result = scan_url(domains, key)
    if ioc is email:
        result = scan_email(emails, key)
    if result:
        print(json.dumps(result, indent=4, sort_keys=True))
    '''


if __name__ == "__main__":
	main(ioc, key)
