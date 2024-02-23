
For a better shell experience.
# Install oh-my-zsh on OpenWrt

Install Requirements Packages

```bash
opkg update && opkg install ca-certificates zsh curl git-http
```

Install oh-my-zsh

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Set zsh as default (thanks to @mlouielu)

```bash
which zsh && sed -i -- 's:/bin/ash:'`which zsh`':g' /etc/passwd
```

## Prevent User Lockout

To prevent lock-outs after accidentially removing zsh([as explained in the wiki][openwrt-wiki-url]) you can add a check for `zsh` and fallback to `ash` in `/etc/rc.local` (thanks to @fox34):

```shell
# Revert root shell to ash if zsh is not available
if grep -q '^root:.*:/usr/bin/zsh$' /etc/passwd && [ ! -x /usr/bin/zsh ]; then
    # zsh is root shell, but zsh was not found or not executable: revert to default ash
    [ -x /usr/bin/logger ] && /usr/bin/logger -s "Reverting root shell to ash, as zsh was not found on the system"
    sed -i -- 's:/usr/bin/zsh:/bin/ash:g' /etc/passwd
fi
```
<!-- appendices -->

[openwrt-wiki-url]: https://openwrt.org/docs/guide-developer/write-shell-script#can_i_change_my_default_shell_from_ash_to_bash 'OpenWrt Wiki'
<!-- end appendices -->


## Plugins

###  zsh-autosuggestions

https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
###  zsh-syntax-highlighting
https://github.com/zsh-users/zsh-syntax-highlighting