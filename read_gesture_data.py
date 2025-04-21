import csv

def read_gesture_data():
    try:
        with open('gesture_data/gesture_data.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            print("Header:", header)
            print("\nFirst few rows:")
            for i, row in enumerate(reader):
                if i < 3:  # Print first 3 rows
                    print(f"Row {i+1}:", row)
                else:
                    break
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    read_gesture_data() 