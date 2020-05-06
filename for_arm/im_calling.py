import os
from for_arm.arm_method import method_for_files
from for_arm.arm_pan17_stylebreach_evaluator import main

"""
from for_arm.arm_pan17_stylebreach_evaluator import main
train_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/train_dataset'
test_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/test_dataset'
train_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/train_results'
test_results_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/test_results'
train_output_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/train_results'
test_output_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/test_results'
"""

add_test_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/add_test_dataset'
auto_train_path = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/data/auto_train_dataset'

add_test_res = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/add_test_results'
auto_train_res = '/Users/hekpo/PycharmProjects/Style_Breach_Detection/for_arm/results/auto_train_results'



input_path=add_test_path
results_path=add_test_res
eval_result_path='/Users/hekpo/Desktop/exper_result'

#use mathod
method_for_files(input_path,results_path,'par','AgglomerativeClustering',n_clusters=2,linkage='ward',affinity='euclidean')

#eval
main(input_path,results_path,eval_result_path)