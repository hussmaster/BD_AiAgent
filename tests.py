from functions.run_python_file import run_python_file


def main():
    test_1 = run_python_file("calculator", "main.py")
    print(test_1)
    test_2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(test_2)
    test_3 = run_python_file("calculator", "tests.py")
    print(test_3)
    test_4 = run_python_file("calculator", "../main.py")
    print(test_4)
    test_5 = run_python_file("calculator", "nonexistent.py")
    print(test_5)
    test_6 = run_python_file("calculator", "lorem.txt")
    print(test_6)

if __name__ == "__main__":
    main()

#test_5 = get_file_content("calculator", "test.txt")
#print(test_5)

