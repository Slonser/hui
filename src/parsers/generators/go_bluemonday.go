package main

import (
	"encoding/json"
	"fmt"
	"os"
	"github.com/microcosm-cc/bluemonday"
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
		p := bluemonday.UGCPolicy()
		sanitizedHTML := p.Sanitize(payload)
		res = append(res, sanitizedHTML)
	}

	outputFile, err := os.Create("../../results_parsers/GO_BLUEMONDAY.json")
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