import sys
import cantools

def process_message(message: str) -> tuple:
    if len(message) < 17 or message[8] != 'x':
        print('file format looks wrong')
        sys.exit()
    else:
        timestamp = message[:8]
        clean_hex = message[9:]

        id_hex = clean_hex[:8]
        data_hex = clean_hex[8:]

        id_int = int(id_hex, 16)
        return timestamp, id_int, data_hex

def run_script(args):
    db = cantools.database.load_file('../monitor/data/dbc/2024CAR.dbc')
    filepath = args[0]
    with open(filepath, 'r') as input_file:
        with open('signals.txt', 'w') as output_file:
            with open('skipped.txt', 'w') as skipped_file:
                for line in input_file:
                    if len(line.strip()) < 17 or 'x' not in line.strip()[:9]:
                        skipped_file.write(line)
                        continue
                    timestamp, can_id, can_data = process_message(line.strip())
                    if can_id == 218103553:
                        skipped_file.write(line)
                        continue
                    try:
                        msg = db.get_message_by_frame_id(can_id)
                    except KeyError:
                        skipped_file.write(line)
                        continue
                    data_bytes = bytes.fromhex(can_data)
                    decoded_signals = msg.decode(data_bytes)
                    for signal in decoded_signals:
                        output_file.write(f'{timestamp}, {signal}, {decoded_signals[signal]}\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 parse_tcu_data.py <path_to_file>')
        sys.exit()
    run_script(sys.argv[1:])
