# scruffy
Leaves your desktop as clean as the Planet Express ✨🧹

![Scruffy the Janitor](https://i.imgur.com/d7iX9qY.png)

## Configuration
Configuration is achieved via environment variables set in a `.scruffyrc` file in your home directory (i.e. `~/.scruffyrc`).  It's invoked prior to executing Scruffy, and can be customized with any valid shell script syntax.

If you do not have a `~/.scruffyrc` file when you run Scruffy, one will be created for you with default values.

### Directives

#### SCRUFFY_DAYS_TO_LEAVE_ON_DESKTOP
Number of daily folders to leave on desktop
```bash
export SCRUFFY_DAYS_TO_LEAVE_ON_DESKTOP=3
```


#### SCRUFFY_DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE
Number of days to check for archival
```bash
export SCRUFFY_DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE=90
```

#### SCRUFFY_SOUND_ON_COMPLETE
Sound to play on completion, corresponds to a file in:
     ~/Library/Sounds
     /System/Library/Sounds 
```bash
export SCRUFFY_SOUND_ON_COMPLETE=Scruffy
```

#### SCRUFFY_UNMOUNT_DISK_IMAGES
Whether or not to unmount disk images as part of cleanup
```bash
export SCRUFFY_UNMOUNT_DISK_IMAGES=False
```
