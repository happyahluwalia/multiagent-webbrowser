# multiagent-webbrowser
Idea is to build a multi-agent web browser: an agentic system with several agents collaborating to solve problems using the web!

              +----------------+
              | Manager agent  |
              +----------------+
                       |
        _______________|______________
       |                              |
  Code interpreter   +--------------------------------+
       tool          |         Managed agent          |
                     |      +------------------+      |
                     |      | Web Search agent |      |
                     |      +------------------+      |
                     |         |            |         |
                     |  Web Search tool     |         |
                     |             Visit webpage tool |
                     +--------------------------------+

Create a web search tool

For web browsing, we can already use our pre-existing DuckDuckGoSearchTool tool to provide a Google search equivalent.

But then we will also need to be able to peak into the page found by the DuckDuckGoSearchTool. To do so, we could import the library's built-in VisitWebpageTool, but we will build it again to see how it's done.

So let's create our VisitWebpageTool tool from scratch using markdownify.

# Build our multi-agent system 🤖🤝🤖

Now that we have all the tools search and visit_webpage, we can use them to create the web agent.

Which configuration to choose for this agent?

    Web browsing is a single-timeline task that does not require parallel tool calls, so JSON tool calling works well for that. We thus choose a ReactJsonAgent.
    Also, since sometimes web search requires exploring many pages before finding the correct answer, we prefer to increase the number of max_iterations to 10.

