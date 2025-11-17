"""Study plan generation crew."""

from crewai import Crew, Task, Process
from datetime import datetime
from typing import Dict, Optional
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from src.agents.extraction_agent import create_extraction_agent
from src.agents.research_agent import create_research_agent
from src.agents.planning_agent import create_planning_agent


class StudyPlanCrew:
    """Crew for generating study plans from assignment details."""
    
    def __init__(self):
        """Initialize the study plan crew with agents."""
        self.extraction_agent = create_extraction_agent()
        self.research_agent = create_research_agent()
        self.planning_agent = create_planning_agent()
        
        logger.info("Initialized StudyPlanCrew")
    
    def create_tasks(self, assignment_text: str, deadline: str, current_date: str) -> list:
        """
        Create tasks for the study plan workflow.
        
        Args:
            assignment_text: The assignment content
            deadline: The deadline date/time
            current_date: Current date
            
        Returns:
            List of Task objects
        """
        # Task 1: Extract assignment details
        extraction_task = Task(
            description=(
                f"Analyze the following assignment text and extract key information:\n\n"
                f"{assignment_text}\n\n"
                f"Extract and structure:\n"
                f"1. Assignment topic/title\n"
                f"2. Course name (if mentioned)\n"
                f"3. Main requirements and deliverables\n"
                f"4. Learning objectives\n"
                f"5. Key topics or areas to study\n"
                f"6. Any specific instructions or constraints\n\n"
                f"Present the information in a clear, organized format."
            ),
            expected_output=(
                "A structured summary containing: assignment topic, course name, requirements, "
                "deliverables, learning objectives, key topics to study, and any special instructions."
            ),
            agent=self.extraction_agent
        )
        
        # Task 2: Research resources
        research_task = Task(
            description=(
                "Based on the extracted assignment details, conduct comprehensive web research to find:\n"
                "1. High-quality tutorials and learning resources\n"
                "2. Video courses or lecture series\n"
                "3. Documentation and reference materials\n"
                "4. Practice exercises and examples\n"
                "5. Community resources (forums, study groups)\n"
                "6. Books or articles (if relevant)\n\n"
                "Focus on resources that are:\n"
                "- Credible and from reputable sources\n"
                "- Suitable for the topic and skill level\n"
                "- Free or accessible to students\n"
                "- Current and up-to-date\n\n"
                "Organize resources by category and provide brief descriptions with URLs."
            ),
            expected_output=(
                "A categorized list of learning resources with titles, descriptions, URLs, "
                "and recommendations for which resources are most essential."
            ),
            agent=self.research_agent,
            context=[extraction_task]
        )
        
        # Task 3: Create study plan
        planning_task = Task(
            description=(
                f"Create a detailed, personalized study plan with the following information:\n\n"
                f"Current Date: {current_date}\n"
                f"Deadline: {deadline}\n\n"
                f"Using the assignment details and research resources, create a comprehensive study plan that:\n\n"
                f"1. Calculates the exact number of days available until the deadline\n"
                f"2. Breaks down the study period into weekly phases\n"
                f"3. For each week, specify:\n"
                f"   - Learning objectives and topics to cover\n"
                f"   - Specific tasks and activities\n"
                f"   - Recommended resources from the research\n"
                f"   - Estimated time commitment (hours per day/week)\n"
                f"   - Milestones or checkpoints\n"
                f"4. Includes buffer time for review and assignment completion\n"
                f"5. Provides practical tips for staying on track\n\n"
                f"Make the plan realistic, actionable, and motivating. Use a clear, easy-to-follow format "
                f"with emojis for visual organization."
            ),
            expected_output=(
                "A comprehensive study plan formatted with:\n"
                "- Executive summary (days remaining, total hours needed)\n"
                "- Weekly breakdown with specific objectives, tasks, resources, and time allocations\n"
                "- Milestones and checkpoints\n"
                "- Success tips and motivational guidance\n"
                "Use markdown formatting with headers, lists, and emojis for readability."
            ),
            agent=self.planning_agent,
            context=[extraction_task, research_task]
        )
        
        return [extraction_task, research_task, planning_task]
    
    def generate_study_plan(
        self, 
        assignment_text: str, 
        deadline: datetime,
        current_date: Optional[datetime] = None
    ) -> Dict:
        """
        Generate a complete study plan.
        
        Args:
            assignment_text: The assignment content
            deadline: The deadline datetime
            current_date: Current datetime (defaults to now)
            
        Returns:
            Dictionary with study plan and metadata
        """
        try:
            if current_date is None:
                current_date = datetime.now()
            
            # Format dates
            deadline_str = deadline.strftime("%B %d, %Y at %I:%M %p")
            current_str = current_date.strftime("%B %d, %Y")
            
            logger.info(f"Generating study plan from {current_str} to {deadline_str}")
            
            # Create tasks
            tasks = self.create_tasks(assignment_text, deadline_str, current_str)
            
            # Create crew
            crew = Crew(
                agents=[self.extraction_agent, self.research_agent, self.planning_agent],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute crew
            result = crew.kickoff()
            
            logger.info("Study plan generation completed successfully")
            
            return {
                "success": True,
                "study_plan": result,
                "deadline": deadline_str,
                "generated_at": current_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating study plan: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
