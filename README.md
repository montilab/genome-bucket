# genome-bucket
AWS Bucket (S3) to Securely Host Files for Genome Web Browsing

This is a prototype for hosting processed ChIP-Seq data (e.g. bigWig) on a CORS-enabled (Cross-Origin Resource Sharing) and encrypted (AES256) AWS S3 Bucket for viewing on the Washington University Epigenome Browser (altering for use with UCSC or IGV browsers is minimal). Modern genome browsers read hosted files that are in an indexed binary format. When sharing ChIP-Seq data with collaborators, providing a simple method to view their data would be ideal.

Here we provide a straightforward solution
  - Process ChIP-Seq data to bigWig format
  - Append a random 64-length ascii key to each file name
  - Generate a datahub configuration file
  - Create and upload renamed files to an encrypted AWS S3 Bucket
  - Upload the datahub configuration file to genome browser

#### Create AWS S3 Bucket
```
aws s3api create-bucket --bucket genome-bucket --region us-east-1
```

#### Generate File Keys and Datahub Config
```
usage: datahub.py [-h] -f FILES [FILES ...] -b BUCKET -r REGION
                  [-n NAMES [NAMES ...]] [-o OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
  -b BUCKET, --bucket BUCKET
  -r REGION, --region REGION
  -n NAMES [NAMES ...], --names NAMES [NAMES ...]
  -o OUTDIR, --outdir OUTDIR
```

*Example*
```
python3 datahub.py -f raw-data/alpha.bigWig \
                      raw-data/beta.bigwig \
                      raw-data/gamma.bigWig \
\
--bucket genome-bucket \
--region us-east-1 \
--names Alpha Beta Gamma \
--outdir data
```

*Datahub Configuration File*
```
[
    {
        "type": "bigwig",
        "name": "Alpha",
        "url": "https://genome-bucket.s3.us-east-1.amazonaws.com/alpha-lpIUCNPdcupkQgdNkp86PBz7bUZ6MJA87BrWSphwLPOEM8rc5VikxliD2qHILKo5.bigWig",
        "options": {
            "color": "black"
        }
    },
    {
        "type": "bigwig",
        "name": "Beta",
        "url": "https://genome-bucket.s3.us-east-1.amazonaws.com/beta-WF277AWwxyQYPEWggTzfepIqDtfIpRy6Uk8I8r3dorVgnYjRrCMhKHOk8FZ3j7Wc.bigwig",
        "options": {
            "color": "black"
        }
    },
    {
        "type": "bigwig",
        "name": "Gamma",
        "url": "https://genome-bucket.s3.us-east-1.amazonaws.com/gamma-09628FsxNzRKNi5tzekzDnupJlPGDowvpwqxwqmFgWyZ79ZhlSCVrptQEesm9mkH.bigWig",
        "options": {
            "color": "black"
        }
    }
]
```

#### Upload Data
```
aws s3 cp data/alpha-lpIUCNPdcupkQgdNkp86PBz7bUZ6MJA87BrWSphwLPOEM8rc5VikxliD2qHILKo5.bigWig s3://genome-bucket/
aws s3 cp data/beta-WF277AWwxyQYPEWggTzfepIqDtfIpRy6Uk8I8r3dorVgnYjRrCMhKHOk8FZ3j7Wc.bigwig s3://genome-bucket/
aws s3 cp data/gamma-09628FsxNzRKNi5tzekzDnupJlPGDowvpwqxwqmFgWyZ79ZhlSCVrptQEesm9mkH.bigWig s3://genome-bucket/
```
