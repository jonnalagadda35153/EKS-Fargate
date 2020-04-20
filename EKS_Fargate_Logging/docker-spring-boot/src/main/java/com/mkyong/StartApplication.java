package com.mkyong;

import com.sumologic.http.aggregation.SumoBufferFlusher;
import com.sumologic.http.sender.ProxySettings;
import com.sumologic.http.sender.SumoHttpSender;
import com.sumologic.http.queue.BufferWithEviction;
import com.sumologic.http.queue.BufferWithFifoEviction;
import java.io.IOException;
import static com.sumologic.http.queue.CostBoundedConcurrentQueue.CostAssigner;
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
        LOG.info("This is a sample log message");
        SpringApplication.run(StartApplication.class, args);
    }

}
