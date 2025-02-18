from util import read_log_file,extract_file,classify_error,get_solution
from llm import get_suggestion


def test():
    try:
        while True:
            err = input("Enter the Error: ")
            print("---------------------------------------------------------------------")
            print("Respose from REGEX:-")
            print(extract_file(err))
            error_type = classify_error(err)
            print(f"Error Type: {error_type}")
            solution = get_solution(error_type)
            print(f"Solution: {solution}")
            print('Response from LLM:-')
            get_suggestion(err)
            print("\n---------------------------------------------------------------------")
    except KeyboardInterrupt as C:
        return




if __name__ == "__main__":
    # log_file = 'logs/sample_log4.txt'
    # log_content = read_log_file(log_file)
    # print(extract_file(log_content))
    # error_type = classify_error(log_content)
    # print(f"Error Type: {error_type}")
    # solution = get_solution(error_type)
    # print(f"Possible Solution: {solution}")
    # llm_suggestion = get_suggestion(log_content)
    # print(llm_suggestion)
    test()
