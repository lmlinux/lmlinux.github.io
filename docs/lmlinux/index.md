**[English](../en/lmlinux/index.md) · [GitHub 项目与完整文档](https://github.com/lmlinux/lmlinux#readme)**

# lmlinux

**内置本地语言模型的 Debian Linux 发行版。**

lmlinux 基于 Debian 13.8.0 live Cinnamon，集成 Qwen3.5-9B Q4_K_M、hax 和 llama-server，面向离线救援，以及无网络环境下的首次安装和首次启动。live 会话及安装后的系统都是普通、完全可写的 Debian，`apt` 可正常使用且变更持久；模型权重在构建时写入镜像，不进入 Git 仓库。

## 当前候选版与验证边界

`13.8.0-rc1` 是候选发布，不是稳定版或 `latest` 版本。这个精确镜像已通过构建完整性检查、独立制品复核、离线 live 启动与安装到硬盘检查，以及离线已安装系统的冷启动、暖缓存追问和 bare-hax 检查。**这些检查并未完成 GA 前仍需通过的行为电池、完整离线救援 / 首次安装、真实用户和外部反馈门槛。**

一次在 16 GiB 内存、4 vCPU 虚拟机上的无人协助离线救援运行约 66 分钟后仍未完成：它把 APT 源改成标有 `[trusted=yes]` 的 HTTP 条目，改动 resolver/NetworkManager 状态，并转向 `dummy0`/veth 修复，最终仍未装上救援夹具。多轮修复可能需要长时间等待，每项特权变更都应先审查。

一次装后启动观察到前台停在 tty1 登录提示，而 LightDM/Cinnamon 正在 VT7 启动；按 Ctrl+Alt+F7 可看到桌面。后来重新安装系统的日志显示 LightDM 在开机约 17 秒和 39 秒请求激活 VT7，但最初观察并未连续记录前台 VT 状态。随后一次全程无键盘输入的全新安装在约 118 秒自动激活图形 VT，并在约 177 秒开始 Cinnamon 用户会话。另一次首次 HDD 启动曾出现未复现的黑屏 / 虚拟终端无响应，需要硬复位；后续终验通过。这些显示现象分开记录，尚未确定同一个根因。

## 下载镜像

镜像以 OCI 制品发布在 GHCR，请使用字面标签 `rc`；没有按版本号命名的 registry 标签，也没有 `latest` 标签。

- 制品：`ghcr.io/lmlinux/lmlinux-iso:rc`
- [GHCR 软件包页面](https://github.com/lmlinux/lmlinux/pkgs/container/lmlinux-iso)
- 文件名：`lmlinux-debian-13.8.0-amd64-cinnamon-live-qwen3.5-9b-q4_k_m-20261125.iso`
- 大小：10,030,678,016 字节（约 9.34 GiB）
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
