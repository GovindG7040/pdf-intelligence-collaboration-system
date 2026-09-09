function SourceList({ sources }) {

    // ==========================================
    // NO SOURCES
    // ==========================================

    if (!sources || sources.length === 0) {

        return null;

    }

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="source-list">

            <p className="source-title">

                Sources

            </p>

            <div className="source-chips">

                {

                    sources.map((source, index) => (

                        <span

                            key={index}

                            className="source-chip"

                        >

                            📄 {source.file}

                        </span>

                    ))

                }

            </div>

        </div>

    );

}

export default SourceList;