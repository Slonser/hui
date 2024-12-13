package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"golang.org/x/net/html"
)

func generate() {
	file, err := os.Open("../../generated_payloads.json")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	var arr []string
	if err := json.NewDecoder(file).Decode(&arr); err != nil {
		fmt.Println("Error decoding JSON:", err)
		return
	}

	var res []string
	for _, payload := range arr {
		htmlContent := fmt.Sprintf("<html><body>%s</body></html>", payload)

		doc, err := html.Parse(strings.NewReader(htmlContent))
		if err != nil {
			fmt.Println("Error parsing HTML:", err)
			continue
		}

		var bodyInnerHTML string
		var f func(*html.Node)
		f = func(n *html.Node) {
			if n.Type == html.ElementNode && n.Data == "body" {
				var buf strings.Builder
				html.Render(&buf, n)
				bodyInnerHTML = buf.String()
			}
			for c := n.FirstChild; c != nil; c = c.NextSibling {
				f(c)
			}
		}
		f(doc)

		res = append(res, strings.TrimSuffix(strings.TrimPrefix(bodyInnerHTML, "<body>"), "</body>"))
	}

	outputFile, err := os.Create("../../results_parsers/GO_HTML.json")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer outputFile.Close()

	if err := json.NewEncoder(outputFile).Encode(res); err != nil {
		fmt.Println("Error encoding JSON:", err)
	}
}

func main() {
	generate()
}