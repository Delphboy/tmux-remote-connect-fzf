# tmux-remote-connect-fzf

An fzf powered remote connection script written in python

## Dependencies

- Python
- fzf

## `config.json`

The python script will read in a `config.json` file that contains the remote servers you want to connect to. It needs to be in the same directory as the python script. See below for an example:

```json
{
  "Server 1": {
    "ssh_connection": "ssh acc1@example.com",
    "session_names": [
      "echo"
    ]
  },
  "Server 2": {
    "ssh_connection": "ssh delphboy@github.com",
    "session_names": [
      "superpixels",
      "image-captioning"
    ]
  },
  "HPC": {
    "ssh_connection": "ssh -i ~/.ssh/id_rsa acc2@hpc.example.com",
    "session_names": [
      "secret-proj-1",
      "secret-proj-2"
    ]
  }
}
```
