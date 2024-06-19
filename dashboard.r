library("shiny")
library("shinydashboard")

header <- dashboardHeader(
    title = "Dynamic UI Example"
)
sidebar <- dashboardSidebar(
    sidebarMenu(
        menuItemOutput("dynamic_sidebar")
    )
)
body <- dashboardBody(
    tabBox(
        tabPanel(
            strong("One")
        ),
        tabPanel(
            strong("Two")
        )
    )
)
ui <- dashboardPage(header, sidebar, body)

server <- shinyServer(function(input, output, session) {
    output$input <- renderUI({})
    outputOptions(output, "input", suspendWhenHidden = FALSE)

    output$dynamic_sidebar <- renderMenu({
        sidebarMenu(
            menuItem(
                "Slider or numeric problem",
                radioButtons("slider_or_numeric",
                    label = "Slider or Numeric Input",
                    choices = c("Slider", "Numeric"),
                    selected = "Slider",
                    inline = TRUE
                ),
                uiOutput("input")
            )
        )
    })
    output$input <- renderUI({
        if (input$slider_or_numeric == "Slider") {
            sliderInput("slider",
                label = "slider",
                min = 0, max = 1,
                value = 0
            )
        } else {
            numericInput("numeric",
                label = "numeric",
                min = 0, max = 1,
                value = 0
            )
        }
    })
})

shinyApp(ui, server)
