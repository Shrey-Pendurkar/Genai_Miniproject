import os
import logging
from pathlib import Path
from config.settings import DEMO_DIR, UPLOADS_DIR
from core.document_processor import DocumentProcessor
from core.vector_store import global_vector_store
from database.models import DocumentModel
from database.db import get_connection

logger = logging.getLogger(__name__)

DEMO_MATERIALS = {
    "OS_Deadlock_Coffman_Conditions.txt": """
A deadlock is a state in which two or more processes are permanently blocked because each holds a resource
that another process in the set needs, forming a circular dependency. Four necessary conditions, called the
Coffman conditions, must hold at the same time for a deadlock to occur: mutual exclusion, hold and wait, no
preemption, and circular wait. Mutual exclusion means at least one resource is held in a non-shareable mode.
Hold and wait means a process holds at least one resource while waiting to acquire others. No preemption means
resources cannot be forcibly taken away and are released only voluntarily. Circular wait means a closed chain
of processes exists in which each process waits for a resource held by the next one. If any one of the four
conditions is broken, a deadlock cannot occur.
""",
    "OS_Deadlock_Prevention.txt": """
Deadlock prevention makes deadlock impossible by ensuring that at least one Coffman condition can never hold:
make resources shareable (mutual exclusion), request all resources at once (hold and wait), allow preemption
of resources (no preemption), or impose a total ordering on resource requests (circular wait). To break hold
and wait, a process must either request all its resources before it starts or release everything it holds
before requesting more. To break circular wait, every resource type is numbered and processes must request
resources in increasing order. The drawbacks of prevention are lower resource utilisation and possible
starvation.
""",
    "OS_Deadlock_Avoidance_Bankers_Algorithm.txt": """
Deadlock avoidance examines each resource request dynamically and grants it only if the system stays in a safe
state, meaning there is some order in which every process can still finish. The best-known method is
Dijkstra's Banker's Algorithm. It uses the Available, Max, Allocation and Need matrices, where Need = Max -
Allocation. A request is granted only if it does not exceed Need or Available and a safe sequence still
exists; otherwise the process must wait. The main limitation of avoidance is that every process must declare
its maximum resource demand in advance.
""",
    "OS_Deadlock_Detection_and_Recovery.txt": """
Deadlock detection and recovery lets the system enter a deadlock, detects it periodically, and then recovers
from it. For resources with a single instance, detection uses a wait-for graph, and a cycle in the graph means
a deadlock exists. For resources with multiple instances, a detection algorithm similar to the Banker's safety
check is used. Recovery is done either by process termination, aborting all deadlocked processes or one at a
time until the cycle is broken, or by resource preemption, taking resources from some processes and rolling
them back. The costs are detection overhead and lost work.
""",
    "OS_Scheduling_FCFS.txt": """
First-Come, First-Served (FCFS) is the simplest CPU scheduling algorithm: processes run in the order they
arrive in the ready queue. It is non-preemptive, so a running process keeps the CPU until it finishes or
blocks. Its main weakness is the convoy effect, where many short processes wait behind one long CPU-bound
process, which increases the average waiting time. FCFS is easy to implement with a FIFO queue but is a poor
choice for interactive systems.
""",
    "OS_Scheduling_SJF.txt": """
Shortest Job First (SJF) is a CPU scheduling algorithm that always runs the process with the smallest next CPU
burst time, and it gives the minimum average waiting time of any scheduling algorithm. Its drawbacks are that
the burst time must be known or predicted in advance, and that long processes can starve if short ones keep
arriving. The preemptive version is called Shortest Remaining Time First (SRTF).
""",
    "OS_Scheduling_Round_Robin.txt": """
Round Robin (RR) is a preemptive CPU scheduling algorithm in which each process gets the CPU for a fixed time
quantum in turn, and is moved to the back of the ready queue if it has not finished. It is ideal for
time-sharing systems because it gives every process fair, regular CPU time and good response time. Choosing
the quantum is a trade-off: a very large quantum makes Round Robin behave like FCFS, and a very small quantum
causes excessive context-switch overhead.
""",
    "DBMS_Normalization_Purpose.txt": """
Database normalization is a systematic way of organising data in a relational database to reduce data
redundancy and eliminate anomalies. The three anomalies are the insertion anomaly (a fact cannot be added
without unrelated data), the deletion anomaly (deleting a row unintentionally removes other facts) and the
update anomaly (a fact stored in many rows must be changed in every one of them). Normalization works by
decomposing tables using functional dependencies and moving through the normal forms 1NF, 2NF, 3NF and BCNF.
""",
    "DBMS_First_and_Second_Normal_Form.txt": """
First Normal Form (1NF) requires every attribute to hold atomic, indivisible values, with no repeating groups.
Second Normal Form (2NF) requires the table to be in 1NF and every non-key attribute to be fully functionally
dependent on the whole primary key, which eliminates partial dependencies. Partial dependencies can only occur
when the primary key is composite. Example: in OrderItem(OrderID, ProductID, ProductName, Qty), ProductName
depends only on ProductID, so it is moved to a separate Product table.
""",
    "DBMS_Third_Normal_Form_and_BCNF.txt": """
Third Normal Form (3NF) requires the table to be in 2NF and no non-key attribute to be transitively dependent
on the primary key; a transitive dependency is X -> Y and Y -> Z where X is the key. Boyce-Codd Normal Form
(BCNF) is a stricter version of 3NF: for every functional dependency X -> Y, X must be a super key. Every BCNF
table is also in 3NF, but not every 3NF table is in BCNF. Example: Student(StudentID, DeptID, DeptName)
violates 3NF because DeptName depends on DeptID, so DeptName is moved to a separate Department table.
""",
    "DBMS_ACID_Properties.txt": """
ACID properties guarantee reliable database transactions: Atomicity, Consistency, Isolation and Durability.
Atomicity means all operations in a transaction complete or none do (all or nothing), by rolling back on
failure. Consistency means a transaction moves the database from one valid state to another and preserves all
constraints. Isolation means concurrent transactions leave the database in the same state as if they had run
one after another. Durability means that once a transaction commits, its changes persist permanently even
after a system crash. Example: in a bank transfer, the debit and the credit must both succeed or both be
undone.
""",
    "CN_OSI_Model_Layers.txt": """
The OSI reference model divides network communication into seven layers, from bottom to top: Physical, Data
Link, Network, Transport, Session, Presentation and Application. The Physical layer transmits raw bits over
the medium. The Data Link layer handles framing, MAC addressing and error detection (Ethernet, Wi-Fi). The
Network layer does logical IP addressing and routing. The Transport layer provides end-to-end delivery, error
recovery and flow control (TCP, UDP). The Session layer establishes and maintains sessions. The Presentation
layer handles encryption, compression and data format conversion. The Application layer carries user protocols
such as HTTP, FTP, SMTP and DNS.
""",
    "CN_TCP_vs_UDP.txt": """
TCP and UDP are the two main transport layer protocols. TCP (Transmission Control Protocol) is
connection-oriented and reliable: it uses a three-way handshake, guarantees in-order delivery with
acknowledgements and retransmission, and applies flow control and congestion control. UDP (User Datagram
Protocol) is connectionless, lightweight and unreliable: it has no handshake, no ordering guarantee and no
retransmission, so it has lower latency.
""",
    "CN_When_to_Use_TCP_or_UDP.txt": """
Use UDP when low latency matters more than perfect delivery: DNS lookups, live video streaming, voice calls
and online gaming. Use TCP when every byte must arrive correctly and in order: web pages (HTTP and HTTPS),
email, file transfer and remote login. UDP is preferred for real-time traffic because retransmitting a lost
packet would arrive too late to be useful.
""",
    "CN_TCP_Three_Way_Handshake.txt": """
The TCP three-way handshake establishes a connection in three steps: SYN, SYN-ACK, ACK. First the client sends
a SYN segment carrying its initial sequence number. Second the server replies with SYN-ACK, acknowledging the
client's number and sending its own. Third the client sends an ACK and the connection is established. After
that, TCP uses a sliding window for flow control, so the sender never sends more than the receiver's
advertised window, and a congestion window to avoid overloading the network.
""",
    "GenAI_Scaled_Dot_Product_Attention.txt": """
Scaled dot-product attention computes softmax(QK^T / sqrt(d_k)) V, where Q (queries), K (keys) and V (values)
are matrices derived from the input. The query-key dot products give similarity scores, dividing by sqrt(d_k)
keeps them numerically stable, softmax turns them into weights that sum to 1, and the weights are used to mix
the values. Each word therefore gets a dynamic, context-dependent representation built from the words it
attends to.
""",
    "GenAI_Transformer_Architecture.txt": """
The Transformer (Vaswani et al., 2017, Attention Is All You Need) replaced recurrent neural networks (RNNs)
with self-attention, so all words in a sequence are processed in parallel. Multi-head attention runs several
attention heads in parallel so the model can attend to information from different representation subspaces at
once, and the head outputs are concatenated. Positional encodings are added to the word embeddings to inject
word order, because attention by itself has no sense of sequence.
""",
    "GenAI_RAG_Overview.txt": """
Retrieval-Augmented Generation (RAG) combines a retriever with a large language model: relevant passages are
fetched from an external knowledge base and given to the LLM as context, so answers are grounded in real
documents and can cite their sources. This reduces hallucination, although it does not remove it completely.
RAG can use new or private documents without retraining the model.
""",
    "GenAI_RAG_Pipeline_Steps.txt": """
The RAG pipeline has four steps: 1. Document chunking splits text into chunks. 2. Embeddings map chunks into a
vector space using sentence transformers. 3. Similarity search queries a vector database for the top-K most
relevant chunks. 4. Prompt augmentation feeds the retrieved chunks to the LLM together with the question. The
LLM then writes an answer based on those chunks, and the source file and page of each chunk can be shown as a
citation.
""",
    "GenAI_Embeddings.txt": """
An embedding is a dense numeric vector that represents the meaning of a piece of text, so texts with similar
meaning lie close together in vector space. Sentence-transformer models such as all-MiniLM-L6-v2 map text to
384-dimensional vectors. A vector store keeps the chunk vectors and returns the top-K nearest to the query
vector.
""",
    "GenAI_Cosine_Similarity.txt": """
Cosine similarity measures how similar two embedding vectors are by comparing the angle between them: values
near 1 mean very similar meaning, values near 0 mean unrelated. When vectors are normalised to unit length,
cosine similarity equals the dot product. It is the standard measure used to rank chunks against a query in
semantic search.
""",
    "GenAI_Hallucination_Definition.txt": """
An LLM hallucination is a fluent, confident answer that is factually wrong or not supported by any source. It
happens because language models predict likely next words from patterns in their training data and do not
verify facts. Hallucinations are risky in education and exams because a wrong explanation sounds convincing.
""",
    "GenAI_Hallucination_Mitigation.txt": """
How to reduce hallucination in LLMs (hallucination mitigation): use retrieval-augmented generation, instruct
the model to answer only from the provided context and to say when it does not know, cite sources with page
numbers, use a low temperature, and keep a human in the loop to verify important claims. These mitigation
strategies lower the hallucination rate but cannot guarantee zero hallucination. A grounding score estimates
how much of an answer is supported by the retrieved text.
""",
}

def seed_demo_data_if_needed():
    """Seeds CS study files if vector store or DB is empty."""
    existing_docs = DocumentModel.get_all_documents()
    if len(existing_docs) > 0 and global_vector_store.get_chunk_count() > 0:
        return

    logger.info("Seeding CS Demo Data into StudyMind...")
    for fname, content in DEMO_MATERIALS.items():
        file_path = DEMO_DIR / fname
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Process and chunk
        processed = DocumentProcessor.process_and_chunk(file_path)
        doc_id = DocumentModel.add_document(
            filename=fname,
            file_type="txt",
            file_size=len(content),
            page_count=processed["page_count"],
            chunk_count=len(processed["chunks"]),
            topics=["Computer Science", fname.split("_")[0]],
            summary={"Executive Summary": content[:200] + "..."}
        )

        # Add to vector store
        global_vector_store.add_chunks(doc_id, fname, processed["chunks"])
        # Add to DB chunks
        DocumentModel.add_chunks(doc_id, processed["chunks"])

    logger.info("Demo data seeding completed successfully.")

def reseed_demo_data():
    """Wipes ALL indexed documents and the vector index, then re-seeds the demo notes.

    Opt-in only (python -m utils.seed_demo_data --reset). Use it after the demo notes in
    DEMO_MATERIALS change, or when the stored index was built with a different embedding model.
    """
    conn = get_connection()
    conn.execute("DELETE FROM document_chunks")
    conn.execute("DELETE FROM documents")
    conn.commit()
    conn.close()
    global_vector_store.clear()
    seed_demo_data_if_needed()


if __name__ == "__main__":
    import sys
    if "--reset" in sys.argv:
        reseed_demo_data()
    else:
        seed_demo_data_if_needed()
