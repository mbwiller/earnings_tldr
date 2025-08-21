"""
Transcript Processor for EarningsCall-TLDR
Handles document ingestion, cleaning, and chunking for RAG operations
"""

import re
import tiktoken
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TranscriptProcessor:
    """Processes earnings call transcripts for analysis"""
    
    def __init__(self, max_chunk_size: int = 1200, min_chunk_size: int = 500, chunk_overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
        
    def clean_transcript(self, text: str) -> str:
        """Clean and normalize transcript text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common transcript artifacts
        text = re.sub(r'\[.*?\]', '', text)  # Remove timestamps
        text = re.sub(r'\(.*?\)', '', text)  # Remove speaker labels in parentheses
        
        # Normalize speaker names
        text = re.sub(r'([A-Z][A-Z\s]+):', r'\1:', text)
        
        # Remove page numbers and headers
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def extract_speakers(self, text: str) -> List[Dict[str, str]]:
        """Extract speaker segments from transcript"""
        speakers = []
        lines = text.split('\n')
        current_speaker = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line contains speaker name
            speaker_match = re.match(r'^([A-Z][A-Z\s]+):\s*(.*)', line)
            if speaker_match:
                # Save previous speaker's text
                if current_speaker and current_text:
                    speakers.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text)
                    })
                
                # Start new speaker
                current_speaker = speaker_match.group(1).strip()
                current_text = [speaker_match.group(2)]
            else:
                # Continue current speaker's text
                if current_speaker:
                    current_text.append(line)
        
        # Add final speaker
        if current_speaker and current_text:
            speakers.append({
                'speaker': current_speaker,
                'text': ' '.join(current_text)
            })
        
        return speakers
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk text into appropriate sizes for RAG"""
        chunks = []
        tokens = self.tokenizer.encode(text)
        
        i = 0
        while i < len(tokens):
            # Find chunk end
            chunk_end = min(i + self.max_chunk_size, len(tokens))
            
            # Try to break at sentence boundary
            if chunk_end < len(tokens):
                # Look for sentence endings in the overlap region
                overlap_start = max(i + self.max_chunk_size - self.chunk_overlap, i)
                for j in range(chunk_end - 1, overlap_start, -1):
                    if tokens[j] in [self.tokenizer.encode('.')[0], 
                                   self.tokenizer.encode('!')[0], 
                                   self.tokenizer.encode('?')[0]]:
                        chunk_end = j + 1
                        break
            
            # Extract chunk
            chunk_tokens = tokens[i:chunk_end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            # Only add if chunk is large enough
            if len(chunk_tokens) >= self.min_chunk_size:
                chunks.append({
                    'text': chunk_text,
                    'start_token': i,
                    'end_token': chunk_end,
                    'token_count': len(chunk_tokens)
                })
            
            # Move to next chunk with overlap
            i = max(i + 1, chunk_end - self.chunk_overlap)
        
        return chunks
    
    def process_transcript(self, text: str) -> Dict[str, Any]:
        """Process a complete transcript"""
        # Clean the text
        cleaned_text = self.clean_transcript(text)
        
        # Extract speakers
        speakers = self.extract_speakers(cleaned_text)
        
        # Create chunks for RAG
        chunks = self.chunk_text(cleaned_text)
        
        # Extract key sections
        sections = self.extract_sections(cleaned_text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'speakers': speakers,
            'chunks': chunks,
            'sections': sections,
            'metadata': {
                'total_tokens': len(self.tokenizer.encode(cleaned_text)),
                'num_chunks': len(chunks),
                'num_speakers': len(set(s['speaker'] for s in speakers))
            }
        }
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract key sections from transcript"""
        sections = {}
        
        # Look for common section headers
        section_patterns = {
            'prepared_remarks': r'(?:prepared remarks|opening remarks|prepared statement)',
            'qa_section': r'(?:question.?answer|q.?&.?a|questions)',
            'guidance': r'(?:guidance|outlook|forward.?looking)',
            'financial_metrics': r'(?:financial|revenue|earnings|eps|margin)',
            'business_update': r'(?:business update|operational|strategy)'
        }
        
        lines = text.split('\n')
        current_section = 'general'
        current_text = []
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if line matches any section pattern
            matched_section = None
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, line_lower):
                    matched_section = section_name
                    break
            
            if matched_section:
                # Save current section
                if current_text:
                    sections[current_section] = ' '.join(current_text)
                
                # Start new section
                current_section = matched_section
                current_text = [line]
            else:
                current_text.append(line)
        
        # Save final section
        if current_text:
            sections[current_section] = ' '.join(current_text)
        
        return sections
