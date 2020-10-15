# Csgo Data-Collector 
[![C++](https://img.shields.io/badge/language-C%2B%2B-%23f34b7d.svg?style=plastic)](https://en.wikipedia.org/wiki/C%2B%2B) 
[![CS:GO](https://img.shields.io/badge/game-CS%3AGO-yellow.svg?style=plastic)](https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/) 
[![Windows](https://img.shields.io/badge/platform-Windows-0078d7.svg?style=plastic)](https://en.wikipedia.org/wiki/Microsoft_Windows) 
[![x86](https://img.shields.io/badge/arch-x86-red.svg?style=plastic)](https://en.wikipedia.org/wiki/X86) 
[![License](https://img.shields.io/github/license/danielkrupinski/Osiris.svg?style=plastic)](LICENSE)
<br>![Windows](https://github.com/danielkrupinski/Osiris/workflows/Windows/badge.svg?branch=master&event=push)

Software for collecting the position of CS:GO player's bounding boxes and exporting them as csv in realtime.

Free open-source data-collection software for **Counter-Strike: Global Offensive** game. Designed as an internal application - [Dynamic-link library](https://en.wikipedia.org/wiki/Dynamic-link_library) (DLL) loadable into game process. Compatible with the Steam version of the game.

**Although the original software is designed for cheating, this version was developed with the intention of only being used in private matches, causing harm to other player's experience.**

## Prerequisites
Microsoft Visual Studio 2019 (preferably the latest version), platform toolset v142 and Windows SDK 10.0.x.x are required in order to compile Osiris. If you don't have ones, you can download VS [here](https://visualstudio.microsoft.com/) (Windows SDK is installed during Visual Studio Setup).

<details>
<summary> Open this if you want to compile from source and modify the code</summary>
<br>

### Downloading

There are two options of downloading the source code:

#### Without [git](https://git-scm.com) Choose this option if you want pure source and you're not going to contribute to the repo. Download size ~600 kB.
To download source code this way [click here](https://github.com/danielkrupinski/Osiris/archive/master.zip).

#### With [git](https://git-scm.com)

Choose this option if you're going to contribute to the repo or you want to use version control system. Download size ~4 MB. Git is required to step further, if not installed download it [here](https://git-scm.com).

Open git command prompt and enter following command:
```
git clone --depth=1 https://github.com/danielkrupinski/Osiris.git
```
`Osiris` folder should have been succesfully created, containing all the source files.

### Compiling from source

When you have equiped a copy of source code, next step is opening **Osiris.sln** in Microsoft Visual Studio 2019.

Then change build configuration to `Release | x86` and simply press **Build solution**.

If everything went right you should receive `Osiris.dll`  binary file.

### Loading / Injecting into game process

Open your favorite [DLL injector](https://en.wikipedia.org/wiki/DLL_injection) and just inject `Osiris.dll` into `csgo.exe` process.

When injected, menu is openable under `INSERT` key.

### Further optimizations
If your CPU supports AVX / AVX2 / AVX-512 instruction set, you can enable it in project settings. This should result in more performant code, optimized for your CPU. Currently SSE2 instructions are selected in project settings.

## FAQ

### How do I open menu?
Press <kbd>INSERT</kbd> while focused on CS:GO window.

### Where is my config file saved?
Configuration files are saved inside `Osiris` folder in your `Documents` folder (`%USERPROFILE%\Documents\Osiris`). The config is in human readable format and can be edited (e.g, using notepad). Sometimes after updates configuration file needs to be deleted and recreated.

### What hooking methods Osiris uses?
Currently implemented hooking methods are:
- MinHook - trampoline hook
- VmtHook - hook a function directly in a vtable
- VmtSwap - create a copy of a vtable and swap the pointer on the class instance

Hooking implementation files are located in [Hooks](https://github.com/danielkrupinski/Osiris/tree/master/Osiris/Hooks) directory.
</details>

## Collecting data

You can download the already compiled dll, and inject it into the game either with [Extreme injector](https://github.com/master131/ExtremeInjector/releases/tag/v3.7.3) (recommended), or [Xenos Injector](https://github.com/DarthTon/Xenos/releases/tag/2.3.2).

Inside Extreme Injector's configuration menu, change the Injection Method from "Standard Injection" to "Manual Map".

Remember to configurate steam to start CS:GO in [insecure mode](https://csgg.in/csgo-guide-to-launch-options/) (with the "-untrusted") flag), and run the game;

Select the game's instance in the injector, and inject the dll. 

After starting a private match with bots, open the menu with <kbd>INSERT</kbd>, and click on the `ESP` option.
In the ESP menu, you can enable both enemy and ally bounding boxes.

## Acknowledgments

* [Daniel Krupiński](https://github.com/danielkrupinski) for developing and maintaining the open-source original software.
* [ocornut](https://github.com/ocornut) and [contributors](https://github.com/ocornut/imgui/graphs/contributors) for creating and maintaining an amazing GUI library - [Dear imgui](https://github.com/ocornut/imgui).
* [Zer0Mem0ry](https://github.com/Zer0Mem0ry) - for great tutorials on reverse engineering and game hacking

## License

> Copyright (c) 2018-2020 Daniel Krupiński

This project is licensed under the [MIT License](https://opensource.org/licenses/mit-license.php) - see the [LICENSE](https://github.com/danielkrupinski/Osiris/blob/master/LICENSE) file for details.
