﻿# **[我的FB粉絲團](https://www.facebook.com/%E7%B7%9A%E4%B8%8A%E8%A8%82%E8%B3%BC%E9%A3%B2%E6%96%99%E5%B9%B3%E5%8F%B0-1986065674805738/?modal=admin_todo_tour)**
* FSM
![](https://i.imgur.com/rdAmGXQ.png)
---
* How To Run:
	>   * 如果使用local端測試，因為有下載redis，故需要先執行[redis伺服器](https://segmentfault.com/q/1010000003813743)(參考最下方回答建立伺服器) (記得先執行redis-server.exe再執行redis-ci.exe)
	>   * 需額外下載redis, jieba (執行pip install redis, jieba即可)
	>   * 直接port是2002，運行python app.py即可
	
* How To Interact With My Chatbot:
	>   * 一開始隨便輸入文字開啟對話
	>   * 接著會出現三個選項 "點我訂飲料" "點我看菜單" "點我給評論"
	>   * 點我訂飲料: 
	>       * 點下去之後會傳給你菜單，回傳此格式以訂餐: "飲料/杯數/備註"
	>		    * 舉例1: 美式咖啡/1/半糖少冰 ; 舉例2: 抹茶拿鐵/3
	>		* 可重複輸入訂多杯飲料
	>		* 訂完飲料之後，回傳此格式以看訂單: "人名 到店付款" -> (記得中間有空格)
	>		    * 舉例1: 施崇祐 到店付款
	>		* 點開菜單則可以觀看你剛剛訂的飲料，並按下"我已付款並取餐"的按鈕，並等10秒 (模擬到飲料店現場的情況，有用sleep(10)去等)，之後完成此分支
	>    * 點我看菜單
	>        * 點下去之後，會傳給你菜單的網址，可以點進去放大來看，之後完成此分支
	>    * 點我給評論
	>        * 點下去之後，會傳給你評論粉絲團的網址，點下去則重新導向網址，之後完成此分支
