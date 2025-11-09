"""
Bedtime Story Generator using LangGraph.
Main entry point for the story generation workflow.
"""
from dotenv import load_dotenv

from story_engine import generate_story

# Load environment variables (story_engine also loads, but this keeps CLI standalone-friendly).
load_dotenv()

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I had 2 more hours, I would:
1. Add user feedback loop: Allow users to request changes to the generated story and iterate based on their feedback
2. Implement story persistence: Save generated stories with metadata (age, topic, scores) for future reference
3. Add story variations: Generate multiple story versions and let users choose their favorite
4. Enhance safety checks: Add more sophisticated content filtering using additional safety APIs
5. Add story audio generation: Convert stories to audio format for bedtime reading
6. Implement story templates: Pre-defined story structures for common themes (friendship, adventure, etc.)
"""


def main():
    """Main function to run the bedtime story generator."""
    # Get user input
    user_input = input("What kind of story do you want to hear? ")
    age_input = input("What age is this story for? (5-10, default 7): ").strip()
    
    try:
        age = int(age_input) if age_input else 7
        if age < 5 or age > 10:
            age = 7
            print(f"Age out of range, using default: 7")
    except ValueError:
        age = 7
        print(f"Invalid age, using default: 7")
    
    tone_input = input("Preferred tone (optional, e.g., 'cozy bedtime', 'gentle humor'): ").strip()
    tone = tone_input if tone_input else None
    
    print("\nGenerating your story...")
    final_state, final_story = generate_story(
        user_input=user_input,
        age=age,
        tone=tone,
        max_iterations=3
    )
    
    if final_story:
        print("\n" + "="*60)
        print("YOUR BEDTIME STORY")
        print("="*60)
        print(final_story)
        print("="*60)
        
        # Print iteration info if available
        if final_state.iteration_count > 0:
            print(f"\nGenerated in {final_state.iteration_count} iteration(s)")
    else:
        print("\nError: No story was generated.")


if __name__ == "__main__":
    main()
