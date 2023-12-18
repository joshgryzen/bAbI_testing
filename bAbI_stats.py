import os


def getStats(task):
    folder_path = os.getcwd() + f"/{task}"  # Replace with the path to your folder

    # Get a list of all text files in the folder
    text_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not text_files:
        print("No text files found in the folder.")
    else:
        # Initialize variables for computing statistics
        shortest_length = float("inf")  # Initialize with positive infinity
        longest_length = 0
        total_length = 0
        num_files = 0
        shortest_file = ""
        longest_file = ""

        # Iterate through each text file
        for file_name in text_files:
            if "Narrative" in file_name:
                file_path = os.path.join(folder_path, file_name)

                # Read the contents of the file
                with open(file_path, "r") as file:
                    content = file.read()

                # Update statistics
                file_length = len(content)
                if file_length < shortest_length:
                    shortest_length = file_length
                    shortest_file = file_name
                if file_length > longest_length:
                    longest_length = file_length
                    longest_file = file_name

                total_length += file_length
                num_files += 1

        # Compute average length
        average_length = total_length / num_files if num_files > 0 else 0

        # Print the statistics
        print(f"Shortest text file: {shortest_file} ({shortest_length} characters)")
        print(f"Longest text file: {longest_file} ({longest_length} characters)")
        print(f"Average text file length: {average_length:.2f} characters")
        print(f"Total number of text files: {num_files}")


getStats("qa1_single-supporting-fact_train")
