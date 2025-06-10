#!/usr/bin/env python3
"""
Simple Analysis Script for AI Tools Performance
===============================================
Analyzes performance data from NUCPA contest comparing 5 AI programming tools.
Referenced in: "AI Effects on Software Development" research paper.

Tools analyzed:
- ChatGPT (GPT-4o)
- GitHub Copilot (GPT-4.1 API) 
- Gemini (2.5 Flash)
- Claude (Sonnet 4)
- DeepSeek (v3 R1)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import fisher_exact
import itertools

def load_ai_tools_data():
    """Load and preprocess AI tools performance data"""
    print("🔍 Loading AI tools data...")
    
    try:
        df = pd.read_csv('data/ai_tools_2.csv')
        print(f"✅ Data loaded successfully: {df.shape}")
        return df
    except FileNotFoundError:
        print("❌ Error: data/ai_tools_2.csv not found")
        return None

def time_to_seconds(time_str):
    """Convert MM:SS.s format to seconds"""
    if pd.isna(time_str) or time_str == 'rejected':
        return None
    try:
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds = float(parts[1])
        return minutes * 60 + seconds
    except:
        return None

def is_successful(value):
    """Check if submission was successful (not rejected)"""
    return pd.notna(value) and value != 'rejected'

def analyze_performance(df):
    """Analyze AI tools performance on contest problems"""
    print("\n📊 ANALYZING AI TOOLS PERFORMANCE")
    print("=" * 50)
    
    # Extract problem columns (A through P)
    problem_cols = [col for col in df.columns if len(col) == 1 and col.isalpha() and 'A' <= col <= 'P']
    tools = df['Ai_tools'].tolist()
    
    print(f"Problems analyzed: {len(problem_cols)} ({problem_cols[0]} to {problem_cols[-1]})")
    print(f"AI tools tested: {len(tools)}")
    
    # Calculate performance metrics
    results = {}
    
    for tool in tools:
        row = df[df['Ai_tools'] == tool].iloc[0]
        
        successful_problems = 0
        response_times = []
        
        for problem in problem_cols:
            if is_successful(row[problem]):
                successful_problems += 1
                time_sec = time_to_seconds(row[problem])
                if time_sec is not None:
                    response_times.append(time_sec)
        
        success_rate = (successful_problems / len(problem_cols)) * 100
        avg_time = np.mean(response_times) if response_times else 0
        
        results[tool] = {
            'success_rate': success_rate,
            'successful_problems': successful_problems,
            'total_problems': len(problem_cols),
            'avg_response_time': avg_time,
            'response_times': response_times
        }
    
    return results, problem_cols

def display_results(results):
    """Display performance results in ranked order"""
    print("\n🏆 PERFORMANCE RANKING")
    print("-" * 40)
    
    # Sort by success rate
    sorted_tools = sorted(results.keys(), key=lambda x: results[x]['success_rate'], reverse=True)
    
    for i, tool in enumerate(sorted_tools, 1):
        data = results[tool]
        rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1] if i <= 5 else f"{i}."
        
        print(f"{rank_emoji} {tool}")
        print(f"   Success Rate: {data['success_rate']:.1f}% ({data['successful_problems']}/{data['total_problems']})")
        print(f"   Avg Time: {data['avg_response_time']:.1f}s")
        print()

def main():
    """Main analysis function"""
    print("🤖 AI TOOLS PERFORMANCE ANALYSIS")
    print("NUCPA Competitive Programming Contest")
    print("=" * 50)
    
    # Load data
    df = load_ai_tools_data()
    if df is None:
        return
    
    # Analyze performance
    results, problem_cols = analyze_performance(df)
    
    # Display results
    display_results(results)
    
    print(f"\n✅ Analysis complete!")

if __name__ == "__main__":
    main() 