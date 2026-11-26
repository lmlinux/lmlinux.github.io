**[中文](../../lmlinux/index.md) · [GitHub project and full documentation](https://github.com/lmlinux/lmlinux#readme)**

# lmlinux

**A Debian-based Linux distribution with a local language model built in.**

lmlinux is based on Debian 13.8.0 live Cinnamon and integrates Qwen3.5-9B Q4_K_M, hax, and llama-server for offline rescue and for first installation and first boot without a network. Both the live session and an installed system are ordinary, fully writable Debian; `apt` works and changes persist. Model weights are baked into the image at build time and are not stored in the Git repository.

## Current RC and validation boundaries

`13.8.0-rc1` is a release candidate, not a stable or `latest` release. This exact image passed build-integrity checks, an independent artifact review, offline live-boot and install-to-disk checks, and offline installed-system cold-start, warm-follow-up, and bare-hax checks. **These checks do not complete the behavioral, complete offline-rescue/first-install, real-user, or external-feedback gates required before GA.**

One unassisted offline-rescue run on a 16 GiB RAM / 4-vCPU VM did not finish after about 66 minutes: it changed APT sources to HTTP entries marked `[trusted=yes]`, altered resolver/NetworkManager state, and pursued `dummy0`/veth recovery without installing the rescue fixture. Expect long waits and review every proposed privileged change.

An installed-boot observation left a tty1 login prompt in the foreground while LightDM/Cinnamon was starting on VT7; Ctrl+Alt+F7 exposed the desktop. Logs from a later reinstallation show LightDM requesting VT7 activation about 17 and 39 seconds after boot, but the original observation did not continuously record foreground-VT state. A subsequent completely fresh, no-keyboard-input installation activated the graphical VT automatically at about 118 seconds and started the Cinnamon user session at about 177 seconds. A separate initial HDD boot had an unreproduced black-screen/unresponsive-VT transient requiring a hard reset; subsequent final probes passed. These display observations are recorded separately and have not been assigned a common root cause.

## Download the image

The image is published as an OCI artifact on GHCR. Use the literal `rc` tag; there is no versioned registry tag and no `latest` tag.

- Artifact: `ghcr.io/lmlinux/lmlinux-iso:rc`
- [GHCR package page](https://github.com/lmlinux/lmlinux/pkgs/container/lmlinux-iso)
- Filename: `lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso`
- Size: 10,030,678,016 bytes (about 9.34 GiB)
- SHA-256: `2eb28a574c67ce1b9cd6b306162a3f87ca1178ac291e310daa71b2c2bfea7ecd`

Pull and verify it with the [ORAS CLI](https://github.com/oras-project/oras):

```bash
oras pull ghcr.io/lmlinux/lmlinux-iso:rc
printf '%s  %s\n' \
  '2eb28a574c67ce1b9cd6b306162a3f87ca1178ac291e310daa71b2c2bfea7ecd' \
  'lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso' | sha256sum -c -
```

After verification, write the image to a USB stick. Replace `/dev/sdX` with the **whole-device** name of the target USB stick; this command destroys all data on that device:

```bash
sudo dd if=lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso of=/dev/sdX bs=4M conv=fsync status=progress
```

Run the Debian installer from the live desktop to install entirely offline. The 9B model requires **16 GiB of RAM**; allow **40 GiB or more** for the target disk. On the test VM, the installed boot activated the graphical VT at about 118 seconds and started the Cinnamon session at about 177 seconds. Model integrity verification overlaps graphics initialization; llama-server loads the model afterward. Timing varies by hardware, so wait a few minutes; if a tty1 prompt remains, Ctrl+Alt+F7 selects the graphical VT.

## Full project documentation

Assistant usage, privileged-operation boundaries, build instructions, and component licenses are maintained in the project repository rather than duplicated on this site:

- [Project README: installation, `ai` / `ai -c`, `sudo ai`, and building](https://github.com/lmlinux/lmlinux#readme)
- [Live ISO build documentation](https://github.com/lmlinux/lmlinux/tree/main/build/debian)
