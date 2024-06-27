import os

# python predict_inference_api.py --m=bigscience/bloom --t=qa1_single-supporting-fact_test.txt


# No context
# os.system(
#     "python predict_inference_api.py --m=bigscience/bloom --t=qa1_single-supporting-fact_test.txt"
# )
# os.system(
#     "python predict_inference_api.py --m=bigscience/bloom --t=qa2_two-supporting-facts_test.txt"
# )
# os.system(
#     "python predict_inference_api.py --m=bigscience/bloom --t=qa3_three-supporting-facts_test.txt"
# )

# With context
os.system(
    "python predict_inference_api.py --m=bigscience/bloom --t=qa1_single-supporting-fact_test.txt --context"
)
os.system(
    "python predict_inference_api.py --m=bigscience/bloom --t=qa2_two-supporting-facts_test.txt --context"
)
os.system(
    "python predict_inference_api.py --m=bigscience/bloom --t=qa3_three-supporting-facts_test.txt --context"
)
