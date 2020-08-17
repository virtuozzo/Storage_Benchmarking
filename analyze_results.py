#!/usr/bin/python3
import sys
import glob
import csv
import numpy as np

test_variant_r = {
    1: "randread",
    2: "4kread",
    3: "8k7030test",
    4: "4k7030thread1",
    5: "4k1thread1queue",
}

test_variant_w = {
    1: "8k7030test",
    2: "4kwrite",
    3: "4k7030thread1",
}


def help():
    print("Usage analyze_results.py <path to files>")

PRECISION = 3


def main():
    files = glob.glob("*.log")
    read_results = dict()
    write_results = dict()
    for file in files:
   	 content = None
   	 with open(file) as f:
   		 content = f.read().splitlines()

   	 test_num_r = 0
   	 test_num_w = 0
   	 server_read_result = dict()
   	 server_write_result = dict()
   	 if content is not None:
   		 for line in content:
   			 str_line = str(line)
   			 if str_line.startswith("   READ: bw="):
   				 part = str_line.split("(")[1]
   				 part = part.split("/s")[0]
   				 if part[-2] == "M":
   					 part = float(part[:-2])
   				 elif part[-2] == "k":
   					 part = round(float(part[:-2])/1000.0, PRECISION)
   				 elif part[-1] == "B":
   					 part = round(float(part[:-1])/1000000.0, PRECISION)
   				 test_num_r += 1
   				 server_read_result[test_variant_r[test_num_r]] = part
   			 elif str_line.startswith("  WRITE: bw="):
   				 part = str_line.split("(")[1]
   				 part = part.split("/s")[0]
   				 if part[-2] == "M":
   					 part = float(part[:-2])
   				 elif part[-2] == "k":
   					 part = round(float(part[:-2])/1000.0, PRECISION)
   				 elif part[-1] == "B":
   					 part = round(float(part[:-1])/1000000.0, PRECISION)
   				 test_num_w += 1
   				 server_write_result[test_variant_w[test_num_w]] = part

   	 read_results[str(file[18:20])]= server_read_result
   	 write_results[str(file[18:20])] = server_write_result

    print(str(read_results))
    print("++++++++++++++++++++++++++++++++")
    print(str(write_results))
    print("++++++++++++++++++++++++++++++++SUM++++++++++++++++++++++++++++++++")
    sum_result_r = dict()
    for test_type in test_variant_r:
   	 sum_result_r[test_variant_r[test_type]] = 0.0

    for result in read_results:
   	 for test_type in test_variant_r:
   		 if test_variant_r[test_type] in read_results[result]:
   			 sum_result_r[test_variant_r[test_type]] += read_results[result][test_variant_r[test_type]]
   		 else:
   			 print("Not present in summary " + test_variant_r[test_type])

    # Round summary
    for test_type in test_variant_r:
   	 sum_result_r[test_variant_r[test_type]] = round(sum_result_r[test_variant_r[test_type]], PRECISION)

    print("READ result:" + str(sum_result_r))

    sum_result_w = dict()
    for test_type in test_variant_w:
   	 sum_result_w[test_variant_w[test_type]] = 0.0
    for result in write_results:
   	 for test_type in test_variant_w:
   		 sum_result_w[test_variant_w[test_type]] += write_results[result][test_variant_w[test_type]]

    # Round summary
    for test_type in test_variant_w:
   	 sum_result_w[test_variant_w[test_type]] = round(sum_result_w[test_variant_w[test_type]], PRECISION)

    print("WRITE result:" + str(sum_result_w))

    csv_columns = ["VM No"]
    csv_columns += list(test_variant_w.values())
    dict_data = list()
    i = 0
    for res in write_results:
   	 i += 1
   	 row = write_results[res]
   	 row.update({"VM No": i})
   	 dict_data.append(row)

    csv_file = "result_summary_write.csv"
    try:
   	 with open(csv_file, 'w') as csvfile:
   		 writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
   		 writer.writeheader()
   		 for data in dict_data:
   			 writer.writerow(data)
    except IOError:
   	 print("I/O error")


    csv_columns = ["VM No"]
    csv_columns += list(test_variant_r.values())
    dict_data = list()
    i = 0
    for res in read_results:
   	 i += 1
   	 row = read_results[res]
   	 row.update({"VM No": i})
   	 dict_data.append(row)

    csv_file = "result_summary_read.csv"
    try:
   	 with open(csv_file, 'w') as csvfile:
   		 writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
   		 writer.writeheader()
   		 for data in dict_data:
   			 writer.writerow(data)
    except IOError:
   	 print("I/O error")



if __name__ == '__main__':
	main()
