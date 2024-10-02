import sys
import os
import cantools

def process_message(message: str) -> tuple:
    if len(message) < 17 or message[8] != 'x':
        print('Error: CAN Format seems wrong! Skipping line')
        # sys.exit()
    else:
        timestamp = message[:8]
        clean_hex = message[9:]

        id_hex = clean_hex[:8]
        data_hex = clean_hex[8:]

        id_int = int(id_hex, 16)
        return timestamp, id_int, data_hex

def run_script(args):
    db = cantools.database.load_file('2024CAR.dbc')
    filepath = args
    fileName = os.path.basename(filepath)

    # Create the directory to store the parsed files
    output_folder = "parsed_files"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Flag to track if any lines were skipped
    skipped_any = False

    parsed_file_path = os.path.join(output_folder, fileName.strip('.TXT') + '_parsed.txt')
    skipped_file_path = os.path.join(output_folder, fileName.strip('.TXT') + '_skipped_lines.txt')

    with open(filepath, 'r') as input_file:
        with open(parsed_file_path, 'w') as output_file:
            with open(skipped_file_path, 'w') as skipped_file:
                for line in input_file:
                    if len(line.strip()) < 17 or 'x' not in line.strip()[:9]:
                        skipped_file.write(line)
                        skipped_any = True
                        continue
                    try: 
                        timestamp, can_id, can_data = process_message(line.strip())
                    except:
                        print(f"File with wrong format: {parsed_file_path}")
                        print(f"Line: {line}")

                    if can_id == 218103553:
                        skipped_file.write(line)
                        skipped_any = True
                        continue

                    try:
                        msg = db.get_message_by_frame_id(can_id)
                    except KeyError:
                        skipped_file.write(line)
                        skipped_any = True
                        continue

                    try: 
                        data_bytes = bytes.fromhex(can_data)
                        decoded_signals = msg.decode(data_bytes)
                    except:
                        skipped_file.write(line)
                        skipped_any = True
                        continue

                    for signal in decoded_signals:
                        output_file.write(f'{timestamp}, {signal}, {decoded_signals[signal]}\n')
    
    # Check if no lines were skipped and delete the skipped file if it's empty
    if not skipped_any:
        os.remove(skipped_file_path)

if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python3 parse_tcu_data.py <path_to_file>')
        sys.exit()
    if len(sys.argv) == 3:
        if sys.argv[2] == "-All":
            # example: python3 parse_tcu_data.py <pathToFolder> -All
            folder_path = sys.argv[1]
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            # Get the number of files
            number_of_files = len(files)
            print(f"Number of files: {number_of_files}")
            for file_name in files:
                file_path = os.path.join(folder_path, file_name).replace("\\","/")
                run_script(file_path)
    else:
        run_script(sys.argv[1])
