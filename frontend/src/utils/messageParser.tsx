import React from 'react';
import MCQForm from '../components/MCQForm';
import CodeBlock from '../components/CodeBlock';

interface CodePart {
  type: 'code';
  language: string;
  content: string;
}

interface TextPart {
  type: 'text';
  content: string;
}

type MessagePart = CodePart | TextPart;

const extractCodeBlocks = (content: string): MessagePart[] => {
  const regex = /```(\w+)?\n([\s\S]*?)```/g;
  const parts: MessagePart[] = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex, match.index)
      });
    }

    // Add code block with default language if undefined
    parts.push({
      type: 'code',
      language: match[1] || 'plaintext', // Ensure we always have a string
      content: match[2]
    });

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < content.length) {
    parts.push({
      type: 'text',
      content: content.slice(lastIndex)
    });
  }

  return parts;
};

const fixMalformedHtml = (html: string): string => {
  // Fix common issues with malformed MCQ HTML
  return html
    // Fix unclosed form tags
    .replace(/<\/form(?!\s*>)/g, '</form>')
    // Fix unclosed div tags
    .replace(/<\/div(?!\s*>)/g, '</div>')
    // Fix unclosed input tags
    .replace(/<input([^>]*[^/])>(?!\s*<\/input>)/g, '<input$1/>')
    // Ensure proper spacing around tags
    .replace(/>\s+</g, '><')
    .trim();
};

export const parseMessage = (content: string): React.ReactNode => {
  // First check for code blocks
  if (content.includes('```')) {
    const parts = extractCodeBlocks(content);
    return (
      <div className="space-y-4">
        {parts.map((part, index) => {
          if (part.type === 'code') {
            return (
              <CodeBlock
                key={index}
                code={part.content}
                language={part.language} // Now guaranteed to be a string
              />
            );
          } else {
            return parseMessageContent(part.content, index);
          }
        })}
      </div>
    );
  }

  return parseMessageContent(content);
};

const parseMessageContent = (content: string, key?: number): React.ReactNode => {
  // Fix malformed HTML before processing
  const fixedContent = fixMalformedHtml(content);

  // Check if content contains HTML
  if (fixedContent.includes('<')) {
    // Check if it's an MCQ with form and answer
    if (fixedContent.includes('<form') && fixedContent.includes('<div class="answer"')) {
      // Split the content into text parts and MCQ parts
      const parts = fixedContent.split(/<form[\s\S]*?<\/form>/g);
      const mcqs = fixedContent.match(/<form[\s\S]*?<\/form>/g) || [];
      const answers = fixedContent.match(/<div class="answer"[\s\S]*?<\/div>/g) || [];

      return (
        <div key={key} className="space-y-4">
          {parts.map((part, index) => (
            <React.Fragment key={index}>
              {/* Render text content */}
              {part.trim() && <div dangerouslySetInnerHTML={{ __html: part.trim() }} />}
              {/* Render MCQ form if available */}
              {mcqs[index] && (
                <MCQForm
                  formContent={mcqs[index]}
                  answerContent={answers[index] || ''}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      );
    }
    // For non-MCQ HTML content
    return <div key={key} dangerouslySetInnerHTML={{ __html: fixedContent }} />;
  }

  // For plain text content
  return <div key={key}>{fixedContent}</div>;
};
