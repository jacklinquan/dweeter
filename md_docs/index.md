# dweeter
A python module for messaging through the free dweet service.
Dweet is a simple machine-to-machine (M2M) service from [dweet.io](https://dweet.io).

## Installation
`pip install dweeter`

## Usage
```python
>>> from dweeter import Dweeter
>>> dwtr = Dweeter("YOUR MAILBOX", "YOUR KEY")
>>> dwtr.send_data({"STRING DATA": "STRING VALUE", "INT DATA": 100, "FLOAT DATA": 3.14, "BOOL DATA": True})
{'thing': '3e7cb39f82fb1ac29e40b935a3cbbaed', 'created': '2022-05-30T04:15:54.787Z', 'content': {'68fcbe24759c8aeb21633df279049eb441eb7c7bcb8b4645f206f55f659fd198': '3aef3ed5ce517e4da35874b765c989256adf568525d43f8da6c2bab602ec5934c667da430fc4e43705699e57ced03d20a270fef33bfc7d1cc2b4f00255c794f00497d29717499ec0c2296b8b52fbef6e015ac0be42de9c8fdfb5f85a5455412cc14bb40acb0f9eaeb606a027b2de1acf94c630f86b5eac56add50048cad47fe5f1b2a699088153e0bf8aa3247192badc'}, 'transaction': '342e85f2-c4dc-4831-a746-e45f50885092'}
>>> dwtr.get_new_data()
{'STRING DATA': 'STRING VALUE', 'INT DATA': 100, 'FLOAT DATA': 3.14, 'BOOL DATA': True, 'remote_time': '2022-05-30T04:15:49.000Z', 'created_time': '2022-05-30T04:15:54.787Z'}
```
