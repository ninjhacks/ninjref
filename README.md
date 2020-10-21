<p align="center">
  <img alt="Ninjref" src="https://i.imgur.com/rSlKlAq.png" height="140" />
  <p align="center">
    <a href="https://github.com/python"><img alt="python" src="https://img.shields.io/badge/python-3.6%2B-blue.svg"></a>
    <a href="https://github.com/sharyer/ninjref/blob/master/LICENSE"><img alt="Software License" src="https://img.shields.io/badge/license-GPL--3.0-orange"></a>
    <a href=""><img alt="tested" src="https://img.shields.io/badge/Tested-Linux-success"></a>
    <a href="https://github.com/sharyer/ninjref"><img alt="Release" src="https://img.shields.io/badge/version-1.2-red.svg"></a>
  </p>
</p>

Ninjref is a fast & light tool for finding urls with reflected parameters from wayback & CommonCrawl it's use threads in threads to optimize it's speed and use Wayback resumption key to divide scan in multiple parts to handle large scan and it's use direct filters on api to get only filtered data from api to do less work on your system. 

## 🚀Features
-   Wayback & CommonCrawl.
-   Power full multithreading.
-   Fully configurable using arguments.
-   Smart matching functionality for anti duplication.
-   Bash pipeline.
-   Advance filters.
-   Wayback resumption key use.

## ✔Installation
```sh

▶ git clone https://github.com/sharyer/ninjref.git
▶ cd ninjref
▶ pip3 install -r requirements.txt
▶ ./ninjref.sh -h

```
## 🧐Usage

```sh
ninjref -h
```

This will display help for the tool.

|        Flag       |                      Description                      |                     Example                     |
| :---------------: | :---------------------------------------------------: | :---------------------------------------------: |
|         -d        |                     Single doimain                    |              ninjref -d example.com             |
|         -f        |                     List of domains                   |              ninjref -f domains.txt             |
|       --od        |           Output dirctory (default : output)          |              ninjref --od output                |
|         -o        |           Output filename (optional)                  |              ninjref -o domains                 |
|       --sd        |           Include subdomain (optional)                |              ninjref --sd                       |
|         -p        |         Providers (default : wayback commoncrawl)     |              ninjref -p wayback                 |
|         -t        |           Main threads counts (default : 1)           |              ninjref -t 1                       |
|       --st        |           Scan threads (default : 10)                 |              ninjref --st 10                    |
|      --wbf        |            (default : statuscode:200 ~mimetype:html)  |              ninjref --filter statuscode:200    |
|      --ccf        |            (default : =status:200 ~mime:.*html)       |              ninjref --filter =status:200       |
|     --payload     |      Payload use in scan (default : ninjhacks)        |              ninjref -p ninjhacks               |
|       --wbl       |      Wayback results per request (default : 10000)    |              ninjref --wbl 1000                 |
|       --ops       |            Output Style (default : 0))                |              ninjref --ops 0                    |

#### Output Filename
By default result filename will be given domain & same for domain list but if outpt filename is set than result of all domains save in one file with provided filename.
#### Main Threads
Main threads use for grab urls from providers use only when you are using domain list & be careful while using it because number of main threads multiply with number of scan threads.
#### Scan Threads
Scan threads use for finding reflected parameters in urls use low number of scan threads while using domain list.
#### Payload
Payload use in checking reflected parameters in url use unique payload for better accuracy in scan.
#### Output Style
Output style is use for result output on console.
0 = output everything.
1 = output only results in json format it's can help you using ninjref with other tool by connecting them with bash pipeline.
2 = not results in output use clean status of scan
3 = not errors in output.
#### Filters
Filters directly use on providers to get only useful filtered data from provider to do faster scan and take less power.
|      Wayback      |    Commoncrawl    |                      Description                              |
| :---------------: | :---------------: | :-----------------------------------------------------------: |
|statuscode:200     |   =status:200     | return only those urls which status code is 200               |
|!statuscode:200    |   !=status:200    | return only non 200 status code                               |
|mimetype:text/html |  mime:text/html   | return only those url which response type is text/html        |
|!mimetype:text/html|  !=mime:text/html | return only non text/html response type                       |
|~mimetype:html     |   ~mime:.*html    | return all those url which have html word in response type    |
|~original:ninja    |   ~url:.*ninja    | return all those url which have ninja word in url             |

## 📄License

The project has signed a GPL-3.0 license, for more information, please read [LICENSE](https://github.com/sharyer/ninjref/blob/master/LICENSE).
