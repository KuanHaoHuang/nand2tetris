# Rscript /Users/WilsonHuang/Downloads/nand2tetris/track_progress.R /Users/WilsonHuang/Downloads/nand2tetris/track_progress.csv
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(lubridate))

args <- commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
    stop("no input?", call.=FALSE)
} else if (length(args)==2) {
    my_csv <- args[1]
    if (!file.exists(my_csv) | !endsWith(my_csv, ".csv")) {
        stop("input file not existing or not being csv?", call.=FALSE)
    }
    yyyy_mm <- args[2]
    if (!grepl(yyyy_mm, pattern = "-") | !(nchar(yyyy_mm) == 7)) {
        stop("course_starts_in_yyyy-mm: wrong format?", call.=FALSE)
    }
    yyyy <- strsplit(yyyy_mm, "-")[[1]][1]
    mm <- strsplit(yyyy_mm, "-")[[1]][2]
    if (is.na(as.numeric(yyyy)) | is.na(as.numeric(mm))) {
        stop("course_starts_in_yyyy-mm: wrong year or month format?", call.=FALSE)
    }
    yyyy <- as.integer(yyyy)
    mm <- as.integer(mm)
} else {
    stop("not exactly two arguments? (csv_path, course_starts_in_yyyy-mm)", call.=FALSE)
}

# my_csv <- "/Users/WilsonHuang/Downloads/nand2tetris/track_progress.csv"
dat <- suppressMessages(read_csv(my_csv))
lct <- Sys.getlocale("LC_TIME")
Sys.setlocale("LC_TIME", "C")
dat <- dat %>% 
    mutate(
        created_date = created_time %>% strptime(format = "%a %b %e %H:%M:%S %Y") %>% lubridate::date(),
        last_modified_date = last_modified_time %>% strptime(format = "%a %b %e %H:%M:%S %Y") %>% lubridate::date()
    ) %>% 
    select(-ends_with("_time"))
dat$proj_name <- dat$file_path %>% sapply(
    function(x) {
        spl <- strsplit(x, "/")[[1]]
        ind <- grep(spl, pattern = "projects")
        if (length(ind) != 1) {
            return("")
        }
        ind <- ind + 1
        proj_name <- spl[ind]
        if (is.na(suppressWarnings(as.numeric(proj_name)))) {
            return("")
        }
        return(proj_name);
    }
)
course_starts_date <- dat$created_date %>% min
proj_tbl <- 
    tribble(
        ~proj_name, ~proj_desc,
        "00", "00 Course Starts!",
        "01", "01 Boolean Logic",
        "02", "02 Boolean Arithmetic",
        "03", "03 Sequential Logic",
        "04", "04 Machine Language",
        "05", "05 Computer Architecture",
        "06", "06 Assembler",
        "07", "07 VM I: Stack Arithmetic",
        "08", "08 VM II: Program Control",
        "09", "09 High-Level Language",
        "10", "10 Compiler I: Syntax Analysis",
        "11", "11 Compiler II: Code Generation",
        "12", "12 Operating System"
    )
dat_filt <- dat %>% 
    filter(year(last_modified_date) >= yyyy, month(last_modified_date) >= mm)
dat_plot <- dat_filt %>% 
    filter(proj_name != "") %>% 
    group_by(proj_name) %>% 
    summarise(max_last_modified_date = max(last_modified_date)) %>% 
    ungroup() %>% 
    add_row(proj_name = "00", max_last_modified_date = course_starts_date) %>% 
    left_join(proj_tbl, by = "proj_name") %>% 
    arrange(proj_name) %>% 
    mutate(day_elapsed = (max_last_modified_date - lag(max_last_modified_date)) %>% as.integer,
           text = ifelse(!is.na(day_elapsed), str_c(proj_desc, ": ", day_elapsed, " days"), proj_desc))
dat_plot$label_date_position <- dat_plot$max_last_modified_date
dat_plot$hjust <- "left"
day_dodge <- 6
dat_plot$label_date_position[as.numeric(dat_plot$proj_name) < 7] <- dat_plot$max_last_modified_date[as.numeric(dat_plot$proj_name) < 7] %m+% days(+day_dodge)
dat_plot$label_date_position[as.numeric(dat_plot$proj_name) >= 7] <- dat_plot$max_last_modified_date[as.numeric(dat_plot$proj_name) >= 7] %m+% days(-day_dodge)
dat_plot$hjust[as.numeric(dat_plot$proj_name) >= 7] <- "right"
p <- dat_plot %>% 
    ggplot(aes(max_last_modified_date, proj_name, colour = proj_name)) +
    geom_point(size = 3) +
    geom_text(aes(x = label_date_position, 
                  label = text, 
                  hjust = hjust)) + 
    geom_text(aes(x = course_starts_date,
                  y = "11",
                  label = str_c("It took me ", 
                                (max(dat_plot$max_last_modified_date) - course_starts_date) %>% as.integer, 
                                " days\nto go through this course!")),
              fontface = "bold",
              colour = "#EC3710",
              hjust = "left") +
    guides(colour = FALSE) + 
    ggtitle("My Nand2Tetris Project Progress Timeline") +
    xlab("Latest Modified Date of The Project") + 
    ylab("Project Index") + 
    theme(plot.title = element_text(face = "bold"))
ggsave(plot = p, filename = str_c(dirname(my_csv), "/", "track_progress.png"),
       width = 8, height = 6)
cat(str_c("png saved: ", dirname(my_csv), "/", "track_progress.png"))

cat("\nStart copying my project part")
my_output_dir <- str_c(dirname(my_csv), "/", "my_projects")
if (dir.exists(my_output_dir)) {
    cat("\nError: 'my_projects' already exists;\n")
    cat("Please manually remove it, and try the script again.\n")
    stop("Plot done, copy failed")
}
dir.create(my_output_dir)
dat_filt <- dat_filt %>% filter(!endsWith(file_path, "DS_Store"),
                                proj_name != "")
for (f in dat_filt$file_path) {
    f_out <- str_c(my_output_dir,"/" , strsplit(f, "/projects/")[[1]][2])
    if (grepl(f, pattern = "__pycache__")) {
        next
    }
    if (!dir.exists(dirname(f_out))) {
        dir.create(dirname(f_out), recursive = TRUE)
    }
    file.copy(from = f, to = f_out)
}
cat("\ncopying done\n")
cat("\nRscript done\n")




