# GIT Repository Cloner

This script reads a json file with a set of credentials and clone or pull all the associated repositories: 

The credentials are:
* user: git user
* token: git token
* type: GITHUB, BITBUCKET
* path: root folder to put the files
* enabled: enables/disables an entry

## Example

```json
[
    {
        "user": "example",
        "token": "TOKEN",
        "path": "/home/example/repositories/github",
        "type": "GITHUB",
        "enabled": true
    },
    {
        "user": "example",
        "token": "TOKEN2",
        "path": "/home/example/repositories/bitbucket",
        "type": "BITBUCKET",
        "enabled": false
    }
]
```