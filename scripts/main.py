from convert_pdw5g_csv_to_csv_or_json_for_emulator import convert
import argparse


if __name__ == '__main__':
    #convert('from.csv', 'to.csv /.json', hist_for_emulator=True)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", help="source: .csv", type=str, required=True)
    parser.add_argument("-dst", help="destination: .csv or .json", type=str, required=True)
    parser.add_argument("--emulator", help="histogram for emulator", action='store_true', required=False, default=False)
    args = parser.parse_args()

    path_from = args.src
    path_to = args.dst
    emulator = args.emulator

    convert(path_from, path_to, hist_for_emulator=emulator)
    
    #convert('raw/downlink-5G-3a.csv', 'histograms/downlink-5G-3a_test.csv', hist_for_emulator=True)

