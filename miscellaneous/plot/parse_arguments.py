import argparse

def parse_arguments():
    data={}
    parser = argparse.ArgumentParser(description="Plottet...")

    parser.add_argument("--distribution", help="Distribution", required=True)
    parser.add_argument("--distribution_name", help="Distribution Name", required=True, nargs="+")
    parser.add_argument("--bandwith", help="Bandwith", required=True)
    parser.add_argument("--size", help="Numer of Packages", required=True)
    parser.add_argument("--file", help="File", required=True, action="append", nargs="+")
    parser.add_argument("--name", help="Name", required=True, action="append", nargs="+")
    
    args = parser.parse_args()
    data["distribution"] = args.distribution
    data["distribution_name"] = " ".join(args.distribution_name)
    data["bandwith"] = args.bandwith
    data["size"] = int(args.size)
    data["data"] = {}
    
    for x in range(0, len(args.name)):
        data["data"][args.name[x][0].replace("\"", "").replace("_"," ").replace("Sch Delay", "Sch_Delay")] = args.file[x][0]
     
    return data




