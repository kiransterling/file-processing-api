
import pandas as pd
import os,csv,re,time
from app.modules.pre_processing import pre_process_file

#maintain all file process status
FILE_NAME='status.csv'

#Add delay to test
DELAY=1

def make_df(filename,chunks_size):
    df_header = pd.read_excel(filename, nrows=0)

    chunks = []
    chunk_count = 0
    # First header is read so skip
    skiprows = 1
    while True:
        df_chunk = pd.read_excel(
            filename,
            nrows=chunks_size, skiprows=skiprows, header=None)
        skiprows += chunks_size
        # Break if no data
        if not df_chunk.shape[0]:
            break
        else:
            df_chunk=pre_process_file(df_chunk)  # -->> do pre processing logic
            chunks.append(df_chunk)
        chunk_count += 1

    df_chunks = pd.concat(chunks)
    # Rename the columns to concatenate the chunks with the header.
    columns = {i: col for i, col in enumerate(df_header.columns.tolist())}
    df_chunks.rename(columns=columns, inplace=True)
    df = pd.concat([df_header, df_chunks])
    return df



def process_file(process_id,original_filename):
    fields = [process_id, 'RUNNING']

    # Add entry of file process status in status.csv file
    with open(FILE_NAME, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    filename=process_id+"_"+original_filename
    df = make_df(filename,chunks_size = 1)
    df.to_csv(os.path.splitext(os.path.basename(filename))[0]+".csv")
    os.remove(filename)

    #Added some delay to test
    time.sleep(DELAY)

    # Update file status
    update_file_status(process_id)


def check_file_status(process_id):
   with open(FILE_NAME, 'r', newline='', encoding='utf-8') as file:
      for row in file:
         if(row.split(',')[0]==process_id):
            return (row.split(',')[1].strip())
      return 'NOT_FOUND'

def update_file_status(process_id):
    with open(FILE_NAME, "r+") as file:
        # read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(process_id+',RUNNING'), 0)
        file_contents = text_pattern.sub(process_id+',COMPLETED', file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)





