# silenceofthelambs

A python module that decrypts [shush](https://github.com/realestate-com-au/shush)-like
KMS-encrypted strings stored in the environment, for use in places where using
`shush env` as your entrypoint is not an option, e.g. AWS Lambda.

## Usage

`silenceofthelambs` has two key usages:

1. **Imported and manually activated**
   ```python
   import silenceofthelambs

   # in your main() func, or wherever makes sense
   silenceofthelambs.decrypt()
   ```

   If you want to provide your own boto3 KMS client (e.g. if you need to use different credentials/region):
   ```python
   import silenceofthelambs
   import boto3

   myclient = boto3.client("kms", .....)

   silenceofthelambs.decrypt(kms_client=myclient)
   ```

1. **Imported and automatically activated**

   `silenceofthelambs` also supports auto-activation, using a default boto3 KMS client.
   ```python
   import silenceofthelambs.auto
   ```
