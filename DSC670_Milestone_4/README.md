# Healthcare Data Mapping Assistant

**Student Name:** Shelia Howard  
**Course:** DSC670-T301 Advanced Uses of Generative AI (2271-1)  
**Assignment:** Term Project - Milestone 4  
**Due Date:** Sunday, 11/22/2026 at 11:59 p.m. CT  
**Dataset(s):** `demo_cases.json` contains two authored synthetic examples. Live inference uses synthetic metadata entered in the form. Historical evaluation figures are from the completed Milestone 3 PDF and final Colab notebook, which document `mapping_train.csv` (192), `mapping_validation.csv` (48), `mapping_test.csv` (48), `mapping_challenge.csv` (8), and `mapping_legacy.csv` (30). Runtime does not require those CSVs.

## Assignment coverage

| Professor's request                              | Deliverable                                                                                                                                                   |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Working Streamlit app using the project solution | `app.py` and `mapping.py`. Live inference requires the  saved Milestone 3 checkpoint.                                                                         |
| Source code as one or more Python files          | Both Python files are included at the repository root.                                                                                                        |
| Short PowerPoint with running-app screenshots    | The presentation includes screenshots of the running Streamlit application using the saved fine-tuned checkpoint. Speaker notes provide the narration script. |
| Optional video                                   | The slide notes provide a script.                                                                                                                             |
| Suggested private GitHub submission              | This is located in a currently public repository  for ease of grading                     and Community Cloud instructions appear  below.                     |
| Student-requested companion notebook             | The accompanying notebook documents the implementation and  verifies  the demo data and response checks.                                                      |

This submission follows the Milestone 4 assignment instructions and course rubric. The application uses the model exported from the completed Milestone 3 fine-tuning experiment.

## 1. Run the app locally with the fine-tuned model

1. Unzip the app package and open a terminal in `healthcare_mapping`. Use Python 3.11.
2. Activate the existing project environment.

   These instructions assume a Conda environment named `dsc670` with Python 3.11 is already available.

   ```powershell
   conda activate dsc670
   ```
   
Keep dependency installation in **step 3**, checkpoint setup in **step 4**, and the Streamlit launch command in **step 5**. This removes the premature app launch currently included in step 2.

3. Install the model dependencies. The CPU runtime is sufficient for a smoke test. A CUDA-enabled PyTorch install can be used if your machine already has a compatible GPU/runtime.

   ```sh
   python -m pip install -r requirements-model.txt
   ```

   For the two-example illustrative app only, install `requirements.txt` instead.

4. Download and extract the saved model checkpoint.

   The application uses the model I fully fine-tuned in Milestone 3. The exported checkpoint includes the trained model weights, configuration, and tokenizer files needed to reproduce live inference.

   Download the approximately 2 GB model ZIP from [the saved model checkpoint](https://drive.google.com/drive/folders/1EkUaVpxS2ZVONOwtCsXjqKF7wtf-c9tJ?usp=drive_link). Access is restricted to authorized reviewers. When submitting this repository, I will provide the instructor with download access.

   Extract the ZIP into a folder named `final_model` at the repository root, beside `app.py` and `mapping.py`. Open `final_model` and confirm that `config.json`, the tokenizer files, and the `.safetensors` model weights appear directly inside it. If extraction creates an additional enclosing folder, move its contents into `final_model`.

   Alternatively, keep the extracted files elsewhere and set `MAPPING_MODEL_DIR` to their location before starting the application. For example, in PowerShell:

   ```powershell
   $env:MAPPING_MODEL_DIR = "C:\Models\DSC670\final_model"
   python -m streamlit run app.py
   ```

   After starting the app, select **Live Qwen checkpoint** to generate recommendations using the saved model. The smaller Milestone 3 evidence ZIP contains evaluation records. Live inference requires the full model export described above.
5. Start Streamlit.

   ```sh
   python -m streamlit run app.py
   ```

6. Open `http://localhost:8501`. Select **Live Qwen checkpoint**. Enter synthetic metadata and select **Generate recommendation**. The first request loads the weights. Try both inputs below.

| Field name | Datatype | Description         | Optional synthetic value | Reference decision |
| ---------- | -------- | ------------------- | ------------------------ | ------------------ |
| patientDOB | date     | Patient date of     | 1990-04-11               | date_of_birth      |
|            |          | birth               |                          |                    |
| full_name  | string   | Full legal name in  | Taylor Morgan Example    | REVIEW             |
|            |          | one field           |                          |                    |

   These are reference decisions. Record the checkpoint's actual output if it differs. Confirm that malformed output, if observed, goes to review. Use **Hold**, **Reject**, **Revise**, or **Accept** when a target is proposed. Download the decision as JSON and confirm that the analyst decision is separate from the recommendation.
   
7. The presentation includes live Streamlit screenshots showing a date-of-birth recommendation and a full-name field requiring analyst review. The notebook records both expected decisions with `contract valid=True`.

## 2. Set up a private Streamlit Community Cloud app

1. Make a private GitHub repository. Add `app.py`, `mapping.py`, `demo_cases.json`, `requirements.txt`, `.gitignore`, and `README.md` at its root. Add `requirements-model.txt` only for a live-model setup. GitHub is suggested by the assignment. You can run live locally and submit the Python files and screenshots directly.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and authorize access to the private repository.
3. Select **Create app**, then select your repository, branch, and `app.py` as the entry point. Under **Advanced settings**, select Python 3.11. Deploy.
4. In this configuration Cloud runs the illustrative demo. For a live Cloud instance, the runtime must have access to your exact checkpoint and enough RAM and startup time to load it. The bundled app expects extracted files on the host. A hosted live version needs a secure model provisioning step or a separately hosted inference backend. The notebook outputs and presentation screenshots document live inference with the local checkpoint. The local live workflow is the shortest route to assignment screenshots.
5. The instructor has download access to the folder containing the exported model ZIP.

## 3. Run the companion notebook

Keep the notebook in the repository’s `notebooks` folder or beside `app.py`. Install JupyterLab and ipykernel with `python -m pip install jupyterlab ipykernel`, then launch JupyterLab from the project environment. Run all cells from top to bottom. The submitted notebook uses `RUN_LIVE=True` and includes saved outputs from the exported checkpoint.

## 4. Results

In Milestone 4, both synthetic notebook examples returned the expected decisions and passed response validation. The validator also routed four deliberately invalid responses to REVIEW. The larger Milestone 3 evaluation produced 41 correct targets out of 48 main-test cases, with all 48 responses meeting the JSON contract.

## Submission check

- Include both Python files, the JSON fixtures, dependency files, and setup instructions.
- Attach the PowerPoint. Verify the screenshots and speaker notes before submitting.
- Confirm the instructor's access to any private link you include. Use the due date above.
- Disclose whether the demo used illustrative results or the original checkpoint. Keep the Milestone 3 benchmark measurements separate from these walkthroughs.

Official documentation  
[Deploy on Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)  
[Connect a private GitHub repository](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account)  
[Share a private app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)
