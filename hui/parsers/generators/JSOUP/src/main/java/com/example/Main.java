package com.example;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;
import java.io.FileReader;


public class Main {
    public static void generate() {
        try {
            System.out.println("Starting generation process...");
            JSONParser parser = new JSONParser();
            JSONArray arr = (JSONArray) parser.parse(new FileReader("generated_payloads.json"));
            JSONArray res = new JSONArray();

            for (int i = 0; i < arr.size(); i++) {
                    String htmlContent = (String) arr.get(i);
                    Document doc = Jsoup.parse(htmlContent);
                    String bodyInnerHtml = doc.body().html();
                    res.add(bodyInnerHtml);
            }
            Files.write(Paths.get("results_parsers/JAVA_JSOUP.json"), res.toJSONString().getBytes());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        generate();
    }
}