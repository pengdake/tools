import argparse
import commands
import sys


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("--kind", dest="kind", type=str, help="k8s resource type")
    parse.add_argument("--namespace", dest="namespace", type=str, help="k8s resource namespace")
    parse.add_argument("--key", dest="key", type=str, help="use to filter special k8s resource")
    args = parse.parse_args()
    return args


def get_resource(kind, namespace, key):
    s, o = commands.getstatusoutput('kubectl get %s -n %s | grep "%s" | awk \'{printf %1 "\n"}\'' % (args.kind, args.namespace, args.key))
    if s != 0:
        print("get k8s resource failed\n")
        return
    print o
    return o


def clean_resource(res_list, kind, namespace):
    for res in res_list:
        s, o = commands.getstatusoutput('kubectl delete %s -n %s' % (args.kind, args.namespace))
        if s != 0:
            print("clean %s %s failed" % (args.kind, args.namespace))


if __name__ == "__main__":
    # get special resource
    args = parse_args()
    reses = get_resource(args.kind, args.namespace, args.key)
    if not reses:
        sys.exit(1)
    res_list = reses.split()
    # clean special resource
    clean_resource(res_list, args.kind, args.namespace)
