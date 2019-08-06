import boto3 # s3에 파일을 업로드
import os # 현재 업로드 할 파일 탐색

def upload_files(search_path, target_path):
    session = boto3.Session(
        aws_access_key_id='AKIA56AAHJJ5I7TSHUEG',
        aws_secret_access_key='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',
        region_name='ap-northeast-2'
    )

    s3 = session.resource('s3')
    bucket = s3.Bucket('media.jjjinnn.com')

    for current_dir, sub_dirs, files in os.walk(search_path):
        print(current_dir, sub_dirs, files)

        for file in files:
            full_path = os.path.join(current_dir, file)
            # print(full_path)

            with open(full_path, 'rb') as data:
                # s3 경로
                bucket.put_object(Key=target_path+'/'+(full_path.replace("\\", "/"))[len(search_path)+1:],Body=data, ACL='public-read')


if __name__=="__main__":
    upload_files('./media', 'media')