# lmlinux

=== "中文"

    **内置本地语言模型的 Debian Linux 发行版。**

    lmlinux 基于 Debian 13.8.0 live Cinnamon，面向离线救援，以及无网络环境下的首次安装配置。llama-server 负责 Qwen3.5-9B Q4_K_M 本地推理，hax 负责助手交互及会话保存和恢复；模型权重在构建时写入镜像，不进入 Git 仓库。live 会话及安装后的系统都是普通、完全可写的 Debian，`apt` 可正常使用且变更持久。

    ## 当前候选版与验证边界

    `13.8.0-rc1` 是候选发布，不是稳定版或 `latest` 版本。这个精确镜像已通过构建完整性检查、独立制品复核、离线 live 启动与安装到硬盘检查，以及离线已安装系统的冷启动、暖缓存追问和 bare-hax 检查。**这些检查并未完成 GA 前仍需通过的行为电池、完整离线救援 / 首次安装、真实用户和外部反馈门槛。**

    同一 9B 栈已有两次成功的软件源修复。受控单故障测试只给自然语言请求、不提供修复命令，助手在 16 分 15 秒内把失效的仅 cdrom APT 源替换为 Debian 13 官方源；`apt-get update` 成功，独立更新与软件包解析检查也通过。最后一次安装测试中，用户实测另一次软件源修复约 8 分钟完成。

    两次成功之间进行的另一场压力测试刻意连续叠加多个故障，全程无人干预，用于探索 9B 能力上限，并非重复上述单故障修复。该测试约 66 分钟后仍未完成：它把 APT 源改成标有 `[trusted=yes]` 的 HTTP 条目，改动 resolver/NetworkManager 状态，并转向 `dummy0`/veth 修复，最终仍未装上救援夹具。两次成功修复与这次未完成的压力测试是不同结果，任何一项都不单独代表完整救援场景已验收。多轮修复可能需要长时间等待，每项特权变更都应先审查。

    一次装后启动观察到前台停在 tty1 登录提示，而 LightDM/Cinnamon 正在 VT7 启动；按 Ctrl+Alt+F7 可看到桌面。后来重新安装系统的日志显示 LightDM 在开机约 17 秒和 39 秒请求激活 VT7，但最初观察并未连续记录前台 VT 状态。随后一次全程无键盘输入的全新安装在约 118 秒自动激活图形 VT，并在约 177 秒开始 Cinnamon 用户会话。另一次首次 HDD 启动曾出现未复现的黑屏 / 虚拟终端无响应，需要硬复位；后续终验通过。这些显示现象分开记录，尚未确定同一个根因。

    ## 下载镜像

    镜像以 OCI 制品发布在 GHCR，请使用字面标签 `rc`；没有按版本号命名的 registry 标签，也没有 `latest` 标签。

    - 制品：`ghcr.io/lmlinux/lmlinux-iso:rc`
    - [GHCR 软件包页面](https://github.com/lmlinux/lmlinux/pkgs/container/lmlinux-iso)
    - 文件名：`lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso`
    - 大小：10,030,678,016 字节（约 10.03 GB / 9.34 GiB）
    - SHA-256：`2eb28a574c67ce1b9cd6b306162a3f87ca1178ac291e310daa71b2c2bfea7ecd`

    使用 [ORAS CLI](https://github.com/oras-project/oras) 拉取并校验：

    ```bash
    oras pull ghcr.io/lmlinux/lmlinux-iso:rc
    printf '%s  %s\n' \
      '2eb28a574c67ce1b9cd6b306162a3f87ca1178ac291e310daa71b2c2bfea7ecd' \
      'lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso' | sha256sum -c -
    ```

    校验通过后，可将镜像写入 U 盘。将 `/dev/sdX` 替换为目标 U 盘的**整盘设备**；以下命令会销毁该设备上的全部数据：

    ```bash
    sudo dd if=lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso of=/dev/sdX bs=4M conv=fsync status=progress
    ```

    在 live 桌面运行 Debian 安装器即可完全离线安装。9B 模型需要 **16 GiB 内存**，目标磁盘建议准备 **40 GiB 或更多**。上述测试 VM 的装后启动在约 118 秒激活图形 VT、约 177 秒开始 Cinnamon 会话；模型完整性校验与图形初始化会重叠，而 llama-server 在其后才加载模型。不同硬件耗时会不同，请先等待数分钟；如果仍停在 tty1，可按 Ctrl+Alt+F7 选择图形 VT。

    ## 完整项目文档

    助手用法、特权操作边界、构建方法和组件许可统一维护在项目仓库，不在本站复制：

    - [项目 README：安装、`ai` / `ai -c`、`sudo ai` 与构建](https://github.com/lmlinux/lmlinux#readme)
    - [live ISO 构建文档](https://github.com/lmlinux/lmlinux/tree/main/build/debian)

=== "English"

    **A Debian-based Linux distribution with a local language model built in.**

    lmlinux is based on Debian 13.8.0 live Cinnamon for offline rescue and for first installation and first boot without a network. llama-server provides local Qwen3.5-9B Q4_K_M inference, while hax handles assistant interaction and session save/resume. Model weights are baked into the image at build time and are not stored in the Git repository. Both the live session and an installed system are ordinary, fully writable Debian; `apt` works and changes persist.

    ## Current RC and validation boundaries

    `13.8.0-rc1` is a release candidate, not a stable or `latest` release. This exact image passed build-integrity checks, an independent artifact review, offline live-boot and install-to-disk checks, and offline installed-system cold-start, warm-follow-up, and bare-hax checks. **These checks do not complete the behavioral, complete offline-rescue/first-install, real-user, or external-feedback gates required before GA.**

    Two APT-source repairs succeeded with the same 9B stack. In a controlled single-fault test, the assistant received only a natural-language request, with no repair commands, and replaced a broken cdrom-only APT source with official Debian 13 repositories in 16m15s; `apt-get update` succeeded, and independent update and package-resolution checks passed. In the final installation test, the user observed another APT-source repair complete in about 8 minutes.

    Between those successes, a separate stress test deliberately chained multiple faults to explore the 9B model's limits without human intervention during the attempt. It was not a repeat of the single-fault repair and did not finish after about 66 minutes: it changed APT sources to HTTP entries marked `[trusted=yes]`, altered resolver/NetworkManager state, and pursued `dummy0`/veth recovery without installing the rescue fixture. The two successful repairs and the incomplete stress test are separate results; none alone completes the broader rescue validation. Expect long waits and review every proposed privileged change.

    An installed-boot observation left a tty1 login prompt in the foreground while LightDM/Cinnamon was starting on VT7; Ctrl+Alt+F7 exposed the desktop. Logs from a later reinstallation show LightDM requesting VT7 activation about 17 and 39 seconds after boot, but the original observation did not continuously record foreground-VT state. A subsequent completely fresh, no-keyboard-input installation activated the graphical VT automatically at about 118 seconds and started the Cinnamon user session at about 177 seconds. A separate initial HDD boot had an unreproduced black-screen/unresponsive-VT transient requiring a hard reset; subsequent final probes passed. These display observations are recorded separately and have not been assigned a common root cause.

    ## Download the image

    The image is published as an OCI artifact on GHCR. Use the literal `rc` tag; there is no versioned registry tag and no `latest` tag.

    - Artifact: `ghcr.io/lmlinux/lmlinux-iso:rc`
    - [GHCR package page](https://github.com/lmlinux/lmlinux/pkgs/container/lmlinux-iso)
    - Filename: `lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso`
    - Size: 10,030,678,016 bytes (about 10.03 GB / 9.34 GiB)
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
