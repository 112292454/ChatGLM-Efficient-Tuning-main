// Fetchall fetches URLs in parallel and reports their times and sizes.
package main

import (
	"context"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"
)

var client = http.Client{}

func ExecuteFetchall() {
	FetchAllUrls(os.Args[1:])
}

func FetchAllArgs(url string, bodys []string) []string {
	start := time.Now()
	ch := make(chan string)
	var result []string
	for _, body := range bodys {
		go Post(url, strings.NewReader(body), ch) // start a goroutine
	}
	for range bodys {
		r := <-ch
		result = append(result, r)
		fmt.Printf("%d", r)
	}
	fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())
	return result
}

func FetchAllUrls(urls []string) {
	start := time.Now()
	ch := make(chan string)
	for _, url := range urls {
		go Get(url, ch) // start a goroutine
	}
	for range urls {
		fmt.Println(<-ch) // receive from channel ch
	}
	fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())
}

func Get(url string, ch chan<- string) {
	start := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		ch <- fmt.Sprint(err) // send to channel ch
		return
	}
	nbytes, err := io.Copy(ioutil.Discard, resp.Body)
	resp.Body.Close() // don't leak resources
	if err != nil {
		ch <- fmt.Sprintf("while reading %s: %v", url, err)
		return
	}
	secs := time.Since(start).Seconds()
	ch <- fmt.Sprintf("%.2fs  %7d  %s", secs, nbytes, url)
}

func Post(url string, body io.Reader, ch chan<- string) {
	//start := time.Now()

	request, err := http.NewRequestWithContext(context.Background(), http.MethodGet, url, body)
	if err != nil {
		return
	}
	request.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(request)
	if err != nil {
		ch <- fmt.Sprint(err) // send to channel ch
		return
	}
	res, err := io.ReadAll(resp.Body)
	if err != nil {
		return
	}
	resp.Body.Close() // don't leak resources

	//secs := time.Since(start).Seconds()
	ch <- fmt.Sprintf("%s", res)
}

func SyncPost(url string, body io.Reader) []byte {
	//start := time.Now()

	request, err := http.NewRequestWithContext(context.Background(), http.MethodGet, url, body)
	if err != nil {
		return nil
	}
	request.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(request)
	if err != nil {
		return nil
	}
	res, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil
	}
	resp.Body.Close() // don't leak resources

	//secs := time.Since(start).Seconds()
	return res
}
