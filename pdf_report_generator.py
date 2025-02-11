from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from language_tool_python import LanguageTool

# Initialize the grammar and spelling checker
tool = LanguageTool('en-US')

# Function to read and analyze the file
def read_and_analyze_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
            return lines, total_lines, word_count, char_count
    except FileNotFoundError:
        print("File not found!")
        return None, None, None, None

# Function to check grammar and spelling with line numbers
def check_grammar_and_spelling(lines):
    issues = []
    for i, line in enumerate(lines):
        matches = tool.check(line)
        for match in matches:
            issues.append({
                "line": i + 1,  # Line number (1-based)
                "error": match.ruleId,
                "message": match.message,
                "suggestions": match.replacements,
                "context": match.context
            })
    return issues

# Function to generate the PDF report
def generate_pdf_report(lines, total_lines, word_count, char_count, issues, output_path):
    pdf = canvas.Canvas(output_path, pagesize=letter)
    pdf.setTitle("File Analysis Report")

    # Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 750, "File Analysis Report")

    # Summary Section
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 700, f"Total Lines: {total_lines}")
    pdf.drawString(50, 680, f"Total Words: {word_count}")
    pdf.drawString(50, 660, f"Total Characters: {char_count}")

    # Issues Section
    pdf.drawString(50, 640, "Grammar and Spelling Issues:")
    y_position = 620

    for issue in issues:
        if y_position < 100:  # Add a new page if space runs out
            pdf.showPage()
            y_position = 750
            pdf.setFont("Helvetica", 12)

        # Display error details
        pdf.drawString(120, y_position, f"- Line {issue['line']}: {issue['message']}")
        pdf.drawString(140, y_position - 20, f"  Suggestion: {', '.join(issue['suggestions']) if issue['suggestions'] else 'No suggestion'}")
        y_position -= 40

    # Add right margin for readability
    pdf.drawRightString(50, 100, "End of Report")

    # Save the PDF
    pdf.save()
    print(f"PDF report generated: {output_path}")

# Main function
def main():
    input_file = str(input("Enter the file path to analyze: "))
    output_file = str(input("Enter the name of the output file (e.g., output.pdf): "))
    
    lines, total_lines, word_count, char_count = read_and_analyze_file(input_file)
    if lines is not None:
        issues = check_grammar_and_spelling(lines)
        generate_pdf_report(lines, total_lines, word_count, char_count, issues, output_file)

if __name__ == "__main__":
    main()
