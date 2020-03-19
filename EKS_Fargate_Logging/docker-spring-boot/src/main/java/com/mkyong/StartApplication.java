package com.mkyong;


import org.apache.logging.log4j.*;
import org.apache.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@SpringBootApplication
@Controller
public class StartApplication {

    private static final Logger LOG = Logger.getLogger(StartApplication.class);

    @GetMapping("/")
    public String index(final Model model) {
        model.addAttribute("title", "Docker + Spring Boot");
        model.addAttribute("msg", "Welcome to the docker container!");
        return "index";
    }


    public static void main(String[] args) {
        LOG.debug("I am here");
        LOG.info("This is a sample log message");
        SpringApplication.run(StartApplication.class, args);
    }

}
