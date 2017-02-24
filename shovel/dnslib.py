import dns.resolver

class Dns(object):
    @classmethod
    def get_cname_path(cls, hostname):
        in_list = [hostname]
        out_list = []
        print("Determining CNAME path for %s" % hostname)
        while len(in_list) > 0:
            print("\tIN LIST: %s" % str(in_list))
            print("\tOUT LIST: %s" % str(out_list))
            try:
                target_hostname = in_list.pop()
                out_list.append(target_hostname)
                result = dns.resolver.query(target_hostname, 'CNAME')
                for res in result:
                    print("\tDNS resolver result for %s... %s" % (target_hostname, res))
                    if res not in out_list:
                        print("\tAdding %s to out_list" % res)
                        out_list.append(str(res))
            except Exception as e:
                print("\tException %s in get_cname_path for %s" % (e, hostname))
                pass
        print("Finished CNAME path for %s" % hostname)
        return out_list
