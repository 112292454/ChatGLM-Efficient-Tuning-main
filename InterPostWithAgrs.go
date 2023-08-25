package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type Body struct {
	Database string `json:"database"`
	Sparql   string `json:"sparql"`
}

func main() {
	var sparqls []string

	file, err := os.Open("F:\\正事\\科研训练\\ChatGLM-Efficient-Tuning-main\\data\\CCKS\\generated_predictions.jsonl")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	// 创建一个新的 Scanner
	scanner := bufio.NewScanner(file)

	// 逐行读取文件内容
	for scanner.Scan() {
		line := scanner.Text()
		sparqls = append(sparqls, line)
	}

	fmt.Printf("args number:%d\n", len(sparqls))

	var bodys []string
	for _, sparql := range sparqls {
		b := Body{
			Database: "CCKS",
			Sparql:   sparql,
		}
		jsonData, err := json.Marshal(b)
		if err != nil {
			fmt.Println("Error marshalling to JSON:", err)
			return
		}
		bodys = append(bodys, string(jsonData))
	}
	filePath := "F:\\go\\golearn\\myans.txt"
	file, err = os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	write := bufio.NewWriter(file)

	var succ, notFound, badFormat = 0, 0, 0

	//tempRsp := ch1.FetchAllArgs("http://10.28.236.228:12300/gstore", bodys)
	//fmt.Printf("%d", len(tempRsp))
	//for index, body := range tempRsp {…………………………}
	// 原先使用这里并发查询数据库的结果，然后for一遍看返回值。但是数据库性能不行，会直接把它干挂掉。
	// 所以改为下面的挨个post

	for index, body := range bodys {
		oneRsp := ch1.SyncPost("http://10.112.41.37:12300/gstore", strings.NewReader(body))
		var resp ch1.R
		err := json.Unmarshal(oneRsp, &resp)
		if err != nil {
			fmt.Println("Error unmarshalling JSON:", err)
			return
		}
		var printInfo string
		switch resp.StatusCode {
		case 1001:
			{
				notFound++
				printInfo = "格式正确，但未查询到"
			}
		case 200:
			{
				succ++
				printInfo = "查询成功，结果为："
			}
		case 500:
			{
				badFormat++
				printInfo = "语句格式错误"
			}
		}
		s := sparqls[index]
		record := fmt.Sprintf("\n查询SPARQL：  %s\n%s", s, printInfo)
		if resp.StatusCode == 200 {
			record += getData(resp.Data.Results)

		}
		fmt.Print(record)
		write.Write([]byte(record))
	}
	fmt.Printf("total:%d \t succeed:%d,rate=%d%% \t not found:%d,rate=%d%% \t bad format:%d,rate%d%% \n",
		len(bodys), succ, succ*100.0/len(bodys), notFound, notFound*100.0/len(bodys), badFormat, badFormat*100.0/len(bodys))

}

func getData(results ch1.Results) string {
	res := ""
	for _, v := range results.Bindings {
		l, r := strings.Index(v, "value")+8, len(v)-3
		temp := "<" + v[l:r] + ">\t"
		res += temp
	}
	return res
}
