import subprocess
import time
import json
import os
import argparse
from datetime import datetime

def run_script(script_path):
    start_time = time.time()
    try:
        process = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        end_time = time.time()
        execution_time = end_time - start_time
        return {
            'success': True,
            'execution_time': execution_time,
            'output': process.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': e.stderr
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def compare_workflows(workflow_base_path, iteration, results_dir):
    """Run comparison with iteration number and specified results directory"""
    # Construct paths for both versions
    ray_script = f"{workflow_base_path}_ray.py"
    normal_script = f"{workflow_base_path}.py"
    
    # Check if both files exist
    if not os.path.exists(ray_script) or not os.path.exists(normal_script):
        raise FileNotFoundError(f"One or both script files not found:\n{ray_script}\n{normal_script}")

    # Run both scripts and collect results
    print(f"\nIteration {iteration + 1}/5")
    print(f"Running Ray version: {ray_script}")
    ray_results = run_script(ray_script)
    
    print(f"Running normal version: {normal_script}")
    normal_results = run_script(normal_script)

    # Prepare results dictionary
    results = {
        'iteration': iteration + 1,
        'timestamp': datetime.now().isoformat(),
        'workflow_name': os.path.basename(workflow_base_path),
        'ray_version': {
            'path': ray_script,
            'success': ray_results['success'],
            'execution_time': ray_results.get('execution_time', None) if ray_results['success'] else None,
            'error': ray_results.get('error', None) if not ray_results['success'] else None
        },
        'normal_version': {
            'path': normal_script,
            'success': normal_results['success'],
            'execution_time': normal_results.get('execution_time', None) if normal_results['success'] else None,
            'error': normal_results.get('error', None) if not normal_results['success'] else None
        }
    }

    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)

    # Save individual iteration result
    iteration_filename = f"iteration_{iteration + 1}_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    iteration_path = os.path.join(results_dir, iteration_filename)
    with open(iteration_path, 'w') as f:
        json.dump(results, f, indent=4)

    return results, iteration_path

def run_multiple_comparisons(workflow_base_path, num_iterations=5):
    """Run multiple comparisons and merge results"""
    results_dir = os.path.join(os.path.dirname(workflow_base_path), 'results')
    all_results = []
    all_files = []

    for i in range(num_iterations):
        try:
            result, file_path = compare_workflows(workflow_base_path, i, results_dir)
            all_results.append(result)
            all_files.append(file_path)

            # Print summary for this iteration
            print(f"\nIteration {i + 1} Summary:")
            print("-" * 50)
            if result['ray_version']['success']:
                print(f"Ray version execution time: {result['ray_version']['execution_time']:.2f} seconds")
            else:
                print(f"Ray version failed: {result['ray_version'].get('error')}")
            
            if result['normal_version']['success']:
                print(f"Normal version execution time: {result['normal_version']['execution_time']:.2f} seconds")
            else:
                print(f"Normal version failed: {result['normal_version'].get('error')}")
            
            print(f"Results saved to: {file_path}")

        except Exception as e:
            print(f"Error in iteration {i + 1}: {str(e)}")

    # Calculate averages and merge results
    merged_results = {
        'workflow_name': os.path.basename(workflow_base_path),
        'total_iterations': num_iterations,
        'timestamp_range': {
            'start': all_results[0]['timestamp'],
            'end': all_results[-1]['timestamp']
        },
        'iterations': all_results,
        'summary': {
            'ray_version': {
                'successful_runs': sum(1 for r in all_results if r['ray_version']['success']),
                'average_time': sum(r['ray_version']['execution_time'] for r in all_results if r['ray_version']['success']) / 
                              sum(1 for r in all_results if r['ray_version']['success']) if any(r['ray_version']['success'] for r in all_results) else None
            },
            'normal_version': {
                'successful_runs': sum(1 for r in all_results if r['normal_version']['success']),
                'average_time': sum(r['normal_version']['execution_time'] for r in all_results if r['normal_version']['success']) / 
                               sum(1 for r in all_results if r['normal_version']['success']) if any(r['normal_version']['success'] for r in all_results) else None
            }
        }
    }

    # Save merged results
    merged_filename = f"merged_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    merged_path = os.path.join(results_dir, merged_filename)
    with open(merged_path, 'w') as f:
        json.dump(merged_results, f, indent=4)

    # Print final summary
    print("\nFinal Summary:")
    print("=" * 50)
    print(f"Total iterations completed: {num_iterations}")
    print("\nRay version:")
    print(f"Successful runs: {merged_results['summary']['ray_version']['successful_runs']}/{num_iterations}")
    if merged_results['summary']['ray_version']['average_time']:
        print(f"Average execution time: {merged_results['summary']['ray_version']['average_time']:.2f} seconds")

    print("\nNormal version:")
    print(f"Successful runs: {merged_results['summary']['normal_version']['successful_runs']}/{num_iterations}")
    if merged_results['summary']['normal_version']['average_time']:
        print(f"Average execution time: {merged_results['summary']['normal_version']['average_time']:.2f} seconds")

    print(f"\nAll results saved in: {results_dir}")
    print(f"Merged results saved to: {merged_path}")

def main():
    parser = argparse.ArgumentParser(description='Compare Ray and non-Ray workflow execution times')
    parser.add_argument('workflow_path', type=str, 
                      help='Base path to workflow (without _ray.py or .py extension)')
    
    args = parser.parse_args()
    
    try:
        run_multiple_comparisons(args.workflow_path)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
