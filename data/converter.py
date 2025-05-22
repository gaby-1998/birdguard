import os
import subprocess
import shutil
import zipfile

def convert_xeno(src_dir, dst_dir):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(f'{src_dir}/{f}')]
    print('converting')
    for file in files:
        src_path = f'{src_dir}/{file}'
        dst_path = f'{dst_dir}/{file.removesuffix(".mp3")}.wav'
        print(f'converting: {src_path}')
        command = 'ffmpeg -hide_banner -loglevel error -i "%s" -acodec pcm_s16le -af "pan=mono|FC=FR" -ar 44100 "%s"' % (src_path, dst_path)
        subprocess.call(command, shell=True)

def split(src_dir, dst_dir, duration):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(f'{src_dir}/{f}')]
    print("splitting")
    ind = 0
    for file in files:
        ind = ind + 1
        file_prefix = f'sound_{ind}'
        src_path = f'{src_dir}/{file}'
        dst_path = f'{dst_dir}/{file_prefix}'
        print(f'splitting: {src_path}')
        num_regex = '%03d.wav'
        command = 'ffmpeg -hide_banner -loglevel error -i "%s" -f segment -segment_time %d %s_%s' % (src_path, duration, dst_path,num_regex)
        subprocess.call(command, shell=True)


def copy_specific_duration_file(src_dir, dst_dir, size):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(f'{src_dir}/{f}')]
    print("copying")
    for file in files:
        src_path = f'{src_dir}/{file}'
        dst_path = f'{dst_dir}/{file}'
        file_size = os.path.getsize(src_path)
        if file_size >= size:
            print(f'copying: {src_path}')
            shutil.copyfile(src_path,dst_path)

def copy_esc50_file(src_dir, dst_dir, max_files):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(f'{src_dir}/{f}')]
    print("copying esc50")
    count = 0
    for file in files:
        count = count + 1
        src_path = f'{src_dir}/{file}'
        dst_path = f'{dst_dir}/{file}'
        print(f'copying: {src_path}')
        shutil.copyfile(src_path, dst_path)
        if count == max_files:
            break
def zip_dataset(src_dir,archive_name):
    print("zipping")
    shutil.make_archive(archive_name, 'zip', src_dir)

if __name__ == '__main__':
    duration = 5
    src_main_files_dir = 'src'
    src_esc50_files_dir = 'ESC50'
    src_convert_files_dir = 'convert'
    src_split_files_dir = 'split'
    dst_dir = 'dataset/sparrow'
    dst_esc50_dir = 'dataset/nosparrow'
    dataset_dir = 'dataset'
    dataset_archive = 'dataset'


    try:
        if os.path.isdir(src_convert_files_dir):
            shutil.rmtree(src_convert_files_dir)
        if os.path.isdir(src_split_files_dir):
            shutil.rmtree(src_split_files_dir)
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        if os.path.isdir(dst_esc50_dir):
            shutil.rmtree(dst_esc50_dir)
        if os.path.isfile(dataset_archive):
            os.remove(dataset_archive)
        os.makedirs(src_split_files_dir)
        os.makedirs(src_convert_files_dir)
        os.makedirs(dst_dir)
        os.makedirs(dst_esc50_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        exit(-1)

    convert_xeno(src_main_files_dir,src_convert_files_dir)
    split(src_convert_files_dir,src_split_files_dir,duration)
    copy_specific_duration_file(src_split_files_dir,dst_dir,440625)
    copy_esc50_file(src_esc50_files_dir, dst_esc50_dir, len( os.listdir(dst_dir)))
    zip_dataset(dataset_dir,dataset_archive)
    print("done!")