# Csgo Data-Collector 
[![C++](https://img.shields.io/badge/language-C%2B%2B-%23f34b7d.svg?style=plastic)](https://en.wikipedia.org/wiki/C%2B%2B) 
[![CS:GO](https://img.shields.io/badge/game-CS%3AGO-yellow.svg?style=plastic)](https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/) 
[![Windows](https://img.shields.io/badge/platform-Windows-0078d7.svg?style=plastic)](https://en.wikipedia.org/wiki/Microsoft_Windows) 
[![x86](https://img.shields.io/badge/arch-x86-red.svg?style=plastic)](https://en.wikipedia.org/wiki/X86) 
[![License](https://img.shields.io/github/license/danielkrupinski/Osiris.svg?style=plastic)](LICENSE)
<br>![Windows](https://github.com/danielkrupinski/Osiris/workflows/Windows/badge.svg?branch=master&event=push)

Software for collecting the position of CS:GO player's bounding boxes and exporting them as csv in realtime.

Free open-source data-collection software for **Counter-Strike: Global Offensive** game. Designed as an internal application - [Dynamic-link library](https://en.wikipedia.org/wiki/Dynamic-link_library) (DLL) loadable into game process. Compatible with the Steam version of the game.

**Although the original software is designed for cheating, this version was developed with the intention of only being used in private matches, causing no harm to other player's experiences.**

## Prerequisites
* Microsoft Visual Studio 2019 (preferably the latest version), platform toolset v142 and Windows SDK 10.0.x.x are required in order to run Osiris. If you don't have ones, you can download VS [here](https://visualstudio.microsoft.com/) (Windows SDK is installed during Visual Studio Setup).

* [Python 8.x](https://python.org) with the following additional libraries:
  * mss 
  * numpy 
  * opencv-python 
  * pandas 
After installing python, you can install all the necessary libraries with the following command:
    ```
    pip3 install mss numpy opencv-python pandas
    ```
<details>
<summary> Open this if you want to compile from source and modify the code</summary>
<br>

### Downloading

#### With [git](https://git-scm.com)

Open git command prompt and enter following command:
```
git clone https://github.com/IgaoGuru/csgo-data.git
```
`csgo-data` folder should have been succesfully created, containing all the source files.

### Compiling from source

When you have equiped a copy of source code, next step is opening **Osiris.sln** in Microsoft Visual Studio 2019.

Then change build configuration to `Release | x86` and simply press **Build solution**.

If everything went right you should receive `Osiris.dll`  binary file.

When injected, menu is openable under `INSERT` key.
</details>

## Collecting data

You can download the already compiled dll, and inject it into the game either with [Extreme injector](https://github.com/master131/ExtremeInjector/releases/tag/v3.7.3) (recommended), or [Xenos Injector](https://github.com/DarthTon/Xenos/releases/tag/2.3.2).

Inside Extreme Injector's configuration menu, change the Injection Method from "Standard Injection" to "Manual Map".

Remember to configurate steam to start CS:GO in [insecure mode](https://csgg.in/csgo-guide-to-launch-options/) (with the "-untrusted") flag), and run the game;

Select the game's instance in the injector, and inject the dll. 

After starting a private match with bots, open the menu with <kbd>INSERT</kbd>, and click on the `ESP` option.

In the ESP menu, you can enable either enemy and ally bounding boxes (or both at the same time).
By default, the bounding boxes are not rendered into the game (so you won't be able to see them while playing). Later on, an option for toggling bbox rendering will be added.

After enabling the preffered bounding boxes, a text file will be created in the **stardard path** ` (C:/csgo_log.txt)`. This text file will be read and processed by the `main_cycle.py` script. (You don't need to edit or open the file)

> note: in order to modify the standard csv path, you will need to edit/compile the dll's code from source
<details>
<summary> If you want to modify the standard csv path:</summary>
<br>

After opening the dll's code in VisualStudio, head over to the `StreamProofEsp.cpp` file under the `Hacks` folder. In there, you should find a `PlayerAnnotate` function, and there you can modify the "myfile.open('x')" path.

</details>
## Acknowledgments

* [Daniel Krupiński](https://github.com/danielkrupinski) for developing and maintaining the open-source original software.
* [ocornut](https://github.com/ocornut) and [contributors](https://github.com/ocornut/imgui/graphs/contributors) for creating and maintaining an amazing GUI library - [Dear imgui](https://github.com/ocornut/imgui).
* [Zer0Mem0ry](https://github.com/Zer0Mem0ry) - for great tutorials on reverse engineering and game hacking

## License

> Copyright (c) 2020-2020 Igor Rocha

This project is licensed under the [MIT License](https://opensource.org/licenses/mit-license.php) - see the [LICENSE](https://github.com/danielkrupinski/Osiris/blob/master/LICENSE) file for details.
