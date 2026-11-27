# lmlinux

=== "中文"

    **内置本地语言模型的 Debian Linux 发行版。**

    lmlinux 基于 Debian 13.8.0 live Cinnamon，面向离线救援，以及无网络环境下的首次安装配置。llama-server 负责 Qwen3.5-9B Q4_K_M 本地推理，hax 负责助手交互及会话保存和恢复；模型权重在构建时写入镜像，不进入 Git 仓库。live 会话及安装后的系统都是普通、完全可写的 Debian，`apt` 可正常使用且变更持久。

    ## 当前候选版与验证边界

    - **版本：** `13.8.0-rc1` 是候选发布，不是稳定版或 `latest`。该镜像已通过构建完整性检查、独立制品复核、离线 live 启动与安装检查，以及离线已安装系统的冷启动、暖缓存追问和 bare-hax 检查。**这些检查均未完成 GA 前的行为电池、完整离线救援 / 首次安装、真实用户和外部反馈门槛。**
    - **两次成功的软件源修复：** 受控单故障测试只给自然语言请求，助手在 16 分 15 秒内把失效的仅 cdrom 源替换为 Debian 13 官方源，`apt-get update` 及独立检查通过；最后一次安装测试中，用户实测另一次修复约 8 分钟完成。
    - **未完成的多故障压力测试：** 刻意连续叠加故障探索 9B 上限，约 66 分钟未完成——把 APT 源改为 `[trusted=yes]` HTTP 条目、改动 resolver/NetworkManager、转向 `dummy0`/veth 修复。与上述成功是不同结果；多轮修复等待时间长，每项特权变更应先审查。
    - **进入 GUI 较慢：** 开机时对 5.29 GiB 模型做 SHA-256 校验，与图形初始化重叠；16 GiB 内存、4 vCPU 测试 VM 实测约 2 分钟进入桌面。另一次首次 HDD 启动曾出现未复现的黑屏，需硬复位；后续终验通过。

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

    在 live 桌面运行 Debian 安装器即可完全离线安装。9B 模型需要 **16 GiB 内存**，目标磁盘建议准备 **40 GiB 或更多**。装后首次进入 GUI 较慢（模型完整性校验与图形初始化重叠），测试 VM 上约 2 分钟；不同硬件耗时会不同，请先等待数分钟，若仍停在 tty1，可按 Ctrl+Alt+F7 选择图形 VT。

    ## 完整项目文档

    助手用法、特权操作边界、构建方法和组件许可统一维护在项目仓库，不在本站复制：

    - [项目 README：安装、`ai` / `ai -c`、`sudo ai` 与构建](https://github.com/lmlinux/lmlinux#readme)
    - [live ISO 构建文档](https://github.com/lmlinux/lmlinux/tree/main/build/debian)

=== "English"

    **A Debian-based Linux distribution with a local language model built in.**

    lmlinux is based on Debian 13.8.0 live Cinnamon for offline rescue and for first-time installation and configuration without a network. llama-server provides local Qwen3.5-9B Q4_K_M inference, while hax handles assistant interaction and session save/resume. Model weights are baked into the image at build time and are not stored in the Git repository. Both the live session and an installed system are ordinary, fully writable Debian; `apt` works and changes persist.

    ## Current RC and validation boundaries

    - **Release:** `13.8.0-rc1` is a release candidate, not a stable or `latest` release. This exact image passed build-integrity checks, an independent artifact review, offline live-boot and install-to-disk checks, and offline installed-system cold-start, warm-follow-up, and bare-hax checks. **These checks do not complete the behavioral, complete offline-rescue/first-install, real-user, or external-feedback gates required before GA.**
    - **Two successful APT-source repairs:** in a controlled single-fault test given only a natural-language request, the assistant replaced a broken cdrom-only source with official Debian 13 repositories in 16m15s; `apt-get update` and independent checks passed. In the final installation test, the user observed another repair complete in about 8 minutes.
    - **Incomplete multi-fault stress test:** deliberately chained faults to explore the 9B model's limits; it did not finish after about 66 minutes, switching APT sources to `[trusted=yes]` HTTP entries, altering resolver/NetworkManager state, and pursuing `dummy0`/veth recovery. This is a separate result from the successes above; expect long waits and review every privileged change.
    - **Slow GUI entry:** boot-time SHA-256 verification of the 5.29 GiB model overlaps graphics startup; the 16 GiB RAM / 4-vCPU test VM reached the desktop in about 2 minutes. One initial HDD boot had an unreproduced black-screen transient requiring a hard reset; later probes passed.

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

    Run the Debian installer from the live desktop to install entirely offline. The 9B model requires **16 GiB of RAM**; allow **40 GiB or more** for the target disk. The first GUI entry after installation is slow (model integrity verification overlaps graphics initialization), taking about 2 minutes on the test VM; timing varies by hardware, so wait a few minutes, and if a tty1 prompt remains, Ctrl+Alt+F7 selects the graphical VT.

    ## Full project documentation

    Assistant usage, privileged-operation boundaries, build instructions, and component licenses are maintained in the project repository rather than duplicated on this site:

    - [Project README: installation, `ai` / `ai -c`, `sudo ai`, and building](https://github.com/lmlinux/lmlinux#readme)
    - [Live ISO build documentation](https://github.com/lmlinux/lmlinux/tree/main/build/debian)
